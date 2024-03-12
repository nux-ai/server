import boto3
import json
from config import nux_aws_creds as creds

from utilities.methods import BadRequestError


model_configs = {
    "llama": "meta.llama2-70b-chat-v1"
}


class BedrockClass:
    def __init__(self):
        self.session = boto3.Session(
            aws_access_key_id=creds['aws_access_key'],
            aws_secret_access_key=creds['aws_secret_key'],
            region_name="us-east-1"
        )
        self.client = self.session.client('bedrock-runtime')

    def get_model(self, model_id):
        try:
            response = self.client.get_foundation_model(
                modelIdentifier=model_id
            )
            return response
        except Exception as e:
            raise BadRequestError(str(e))

    def list_models(self, model_provider, ):
        try:
            response = self.client.list_foundation_models()
            return response
        except Exception as e:
            raise BadRequestError(str(e))

    def invoke_model(self,
                     user_input,
                     settings,
                     model_id,
                     content_type='application/json',
                     accept='application/json'
                     ):
        try:
            body = {
                "prompt": user_input,
                **settings
            }
            bytes_object = json.dumps(body).encode('utf-8')
            response = self.client.invoke_model(
                body=bytes_object,
                contentType=content_type,
                accept=accept,
                modelId=model_id
            )
            body_content = response['body'].read()
            return json.loads(body_content)
        except Exception as e:
            raise BadRequestError(str(e))
