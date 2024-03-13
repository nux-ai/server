from fastapi import HTTPException
from config import aws, python_version

from db_internal.service import BaseSyncDBService
from .model import WorkflowCreateRequest

from cloud_services.aws.serverless import LambdaClass

from utilities.code import CodeValidation
from utilities.zipper import PackageZipper
from utilities.helpers import generate_function_name


class CodeHandler:
    def __init__(self, code_as_string, function_name):
        self.code_as_string = code_as_string
        self.function_name = function_name
        self.lambda_client = LambdaClass()
        # self.bucket_name = "nux-code-execution"

    def validate(self):
        # check security
        CodeValidation.check_code_security(self.code_as_string)
        # check for function
        CodeValidation.check_for_function(self.code_as_string)

    async def _create_new_package(self, code_function_name, code_input):
        obj = {
            "function_name": code_function_name,
            "code_as_string": code_input,
            "requirements": self.parsed_settings["requirements"],
            "python_version": self.parsed_settings["python_version"],
        }
        zipper = PackageZipper(obj, self.package_creator_url)
        return zipper.get_s3_url()

    async def create_new_function(self, code_function_name, code_input):
        # first check if lambda exists
        if self.lambda_client.get_function(code_function_name):
            raise HTTPException(detail="Function already exists")

        try:
            # create new package and upload to s3
            function_s3_data = await self._create_new_package(
                code_function_name, code_input
            )

            # create new lambda function
            self.lambda_client.create_with_s3(
                runtime=self.parsed_settings["python_version"],
                function_name=code_function_name,
                s3_bucket=function_s3_data["bucket"],
                s3_key=function_s3_data["key"],
                tags={
                    "Context": "Workbook",
                    "WorkbookId": self.workbook_id,
                    "IndexId": self.index_id,
                },
            )
        except Exception as e:
            raise HTTPException(detail=f"Couldn't create function: {e}")


class WorkflowSyncService(BaseSyncDBService):
    def __init__(self, index_id):
        super().__init__("workflows", index_id)

    def create(self, workflow_request):
        new_workflow = WorkflowCreateRequest(
            code_as_string=workflow_request.code_as_string,
            metadata=workflow_request.metadata,
            settings=workflow_request.settings,
            workflow_name=workflow_request.workflow_name,
        )

        function_name = generate_function_name(self.index_id, new_workflow.workflow_id)

        code_handler = CodeHandler(new_workflow.code_as_string, function_name)
        code_handler.validate()

        code_handler.create_new_function(function_name, new_workflow.code_as_string)

        return self.create_one(new_workflow.model_dump())

    def list(self, lookup_conditions=None, limit=None, offset=None):
        if lookup_conditions is None:
            lookup_conditions = {}
        """List workbooks with pagination."""
        results = self.list_by_index(lookup_conditions, limit, offset)
        return results

    def get(self, workflow_id):
        """Get a single workflow by ID."""
        return self.get_one({"workflow_id": workflow_id})
