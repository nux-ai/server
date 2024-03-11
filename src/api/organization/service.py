from fastapi import BackgroundTasks
from pydantic import ValidationError

from utilities.methods import BadRequestError
from utilities.helpers import generate_api_key
from utilities.encryption import Secret

from cloud_services.notifications.slack import Slack

from config import clerk_credentials
from db.service import sync_db, mongo_client
import requests
from .model import (
    OrganizationBase,
    User,
    UsagePricing,
    DataPermissions,
    ModelPermissions,
    CodePermissions,
    Permissions,
    ApiKey,
    TrustedOrgResponse,
)


class OnboardService:
    def __init__(self):
        pass

    # def __init__(self, background_tasks: BackgroundTasks):
    #     self.background_tasks = background_tasks

    def notify(self, msg):
        Slack.post(msg)

    def lookup_user(self, email):
        pass

    def scrape_website(self, url):
        pass

    def create_workbook(self, org_id, website_id):
        pass


class OrganizationSyncService:
    def __init__(self):
        # Initialize a collection object for 'organizations'.
        self.sync_client = sync_db["organizations"]

    def start_session(self):
        return mongo_client.start_session()

    def create_organization(self, org_metadata={}, users=[]):
        slug = org_metadata["slug"]
        already_exists = self.sync_client.find_one({"metadata.slug": slug})
        if slug is not None and already_exists is not None:
            return already_exists

        # Create permissions and usage objects
        permissions = Permissions(
            code=CodePermissions(),
            models=ModelPermissions(),
            data=DataPermissions(),
            rate_limit="10/minute",
        )
        usage = UsagePricing()
        index = "ix-" + generate_api_key()
        apiKey = ApiKey(name="default", indexes=[index])

        # Create organization with the given metadata, user, and index
        try:
            org = OrganizationBase(
                metadata=org_metadata,
                api_keys=[apiKey],
                indexes=[index],
                users=users,
                permissions=permissions,
                usage=usage,
            )
        except ValidationError as e:
            raise BadRequestError(detail=f"Error parsing the org {str(e.json())}")

        # Insert the organization object into the database
        self.sync_client.insert_one(org.model_dump(by_alias=True))

        return org

    def add_new_membership(self, clerk_org_id, email, user_metadata={}, session=None):
        org = self.sync_client.find_one({"metadata.id": clerk_org_id})
        if not org:
            raise BadRequestError("Organization not found")

        previous_user_exists = self.sync_client.find_one(
            {"org_id": org["org_id"], "users.email": email}
        )
        if previous_user_exists:
            return org
            # raise BadRequestError("User already exists in organization")

        user = User(email=email, metadata=user_metadata)
        self.sync_client.update_one(
            {"org_id": org["org_id"]},
            {"$addToSet": {"users": user.model_dump(by_alias=True)}},
            session=session,
        )

        # background tasks to make onboarding better
        onboarding = OnboardService()
        onboarding.notify(f"🚀 New User!!! {email} created an account")
        # website_url = onboarding.lookup_user(email)
        # website_id = onboarding.scrape_website(website_url)
        # onboarding.create_workbook(org["org_id"], website_id)

        return org

    def delete_organization(self, org_id):
        # Find the organization by its ID
        org = self.sync_client.find_one({"org_id": org_id})

        # Raise an error if the organization is not found
        if not org:
            raise BadRequestError("Organization not found", status_code=400)

        # Delete the organization from the database
        self.sync_client.delete_one({"_id": org["_id"]})

        return True

    def delete_organization_by_clerk_id(self, clerk_org_id):
        # Find the organization by its ID
        org = self.sync_client.find_one({"metadata.id": clerk_org_id})

        # Raise an error if the organization is not found
        if not org:
            raise BadRequestError("Organization not found", status_code=400)

        # Delete the organization from the database
        self.sync_client.delete_one({"_id": org["_id"]})

        return True

    def delete_organization_of_user(self, user_email):
        # Find the organization by its ID
        org = self.sync_client.find_one({"users.email": user_email})

        # Raise an error if the organization is not found
        if not org:
            raise BadRequestError("Organization not found", status_code=400)

        # Delete the organization from the database
        self.sync_client.delete_one({"_id": org["_id"]})

        return True

    def get_by_api_key(self, api_key):
        obj = self.sync_client.find_one({"api_keys.key": api_key})

        # Raise an error if no user is found with the given API key.
        if obj is None:
            raise BadRequestError("API key does not exist")

        # ensure org has credits
        if obj["usage"]["credits"] <= 0:
            raise BadRequestError("No credits remaining")

        return obj

    def get_index_ids(self, api_key, index_id=None):
        obj = self.get_by_api_key(api_key)

        if not obj["indexes"]:
            raise BadRequestError("No index_ids for user")
        if index_id and index_id in obj["indexes"]:
            return index_id
        elif index_id:
            raise BadRequestError("Provided index not found")

        # temp until we can handle multiple index_ids
        return obj["indexes"][0], obj

    def get_by_email(self, email):
        # Retrieve an organization object by a user's email.
        response = list(self.sync_client.find({"users.email": email}))

        # Return None if no organization is found.
        if not response:
            return None

        return OrganizationBase(**response[0])

    def reduce_credit_by_one(self, org_id):
        # Decrement the credit count of an organization by one.
        self.sync_client.update_one(
            {"org_id": org_id, "credits_remaining": {"$gte": 0}},
            {"$inc": {"credits_remaining": -1}},
        )

    def get_by_index_id(self, index_id):
        # Retrieve an organization object by its index_id.
        response = self.sync_client.find_one({"indexes": index_id})

        # Return None if no organization is found.
        if not response:
            raise BadRequestError(detail="Organization not found", status_code=400)

        org = OrganizationBase(**response)
        return org

    def get_for_frontend(self, index_id):
        # Retrieve an organization object by its index_id.
        response = self.sync_client.find_one({"indexes": index_id})

        # Return None if no organization is found.
        if not response:
            raise BadRequestError(detail="Organization not found", status_code=400)

        return TrustedOrgResponse(**response)

    def add_secret(self, index_id, secret_name, secret_value):
        encrypt = Secret()
        organization = self.get_by_index_id(index_id).dict()

        encrypted_secret = encrypt.encrypt_string(secret_value)

        secret = {"name": secret_name, "value": encrypted_secret}

        self.sync_client.update_one(
            {"org_id": organization["org_id"]}, {"$push": {"secrets": secret}}
        )

    def delete_secret(self, index_id, secret_name):
        organization = self.get_by_index_id(index_id).dict()

        self.sync_client.update_one(
            {"org_id": organization["org_id"]},
            {"$pull": {"secrets": {"name": secret_name}}},
        )

    def get_secret(self, index_id, secret_name):
        encrypt = Secret()
        organization = self.get_by_index_id(index_id).dict()

        # Find the organization with the given org_id and secret name
        result = self.sync_client.find_one(
            {"org_id": organization["org_id"], "secrets.name": secret_name},
            {"secrets.$": 1},
        )

        if result is not None and "secrets" in result and len(result["secrets"]) > 0:
            secret_value = result["secrets"][0]["value"]
            return encrypt.decrypt_string(secret_value)
        else:
            raise BadRequestError("Secret not found")
