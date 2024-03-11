from fastapi import BackgroundTasks
from pydantic import ValidationError

from utilities.methods import BadRequestError
from utilities.helpers import generate_api_key
from utilities.encryption import Secret

from db.service import sync_db, mongo_client
from .model import (
    OrganizationBase,
    User,
    UsagePricing,
    Permissions,
    ApiKey,
    TrustedOrgResponse,
)


class OrganizationSyncService:
    def __init__(self):
        self.sync_client = sync_db["organizations"]

    def start_session(self):
        return mongo_client.start_session()

    def create_organization(self, metadata={}, users=[]):
        slug = metadata.get("slug", None)
        already_exists = self.sync_client.find_one({"metadata.slug": slug})
        if slug is not None and already_exists is not None:
            return already_exists

        # Create permissions and usage objects
        permissions = Permissions(rate_limit="10/minute")
        usage = UsagePricing()
        index = "ix-" + generate_api_key()
        apiKey = ApiKey(name="default", indexes=[index])

        # Create organization with the given metadata, user, and index
        try:
            org = OrganizationBase(
                metadata=metadata,
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

    def delete_organization(self, org_id):
        # Find the organization by its ID
        org = self.sync_client.find_one({"org_id": org_id})

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
        organization = self.get_by_index_id(index_id).model_dump()

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
