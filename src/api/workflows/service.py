from fastapi import HTTPException
from config import aws, python_version

from db_internal.service import BaseSyncDBService

from .model import WorkflowCreateRequest
from .utilities import CodeHandler


from utilities.helpers import generate_function_name, current_time


class WorkflowSyncService(BaseSyncDBService):
    def __init__(self, index_id):
        super().__init__("workflows", index_id)

    def create(self, workflow_request):
        # init workflow class
        new_workflow = WorkflowCreateRequest(
            code_as_string=workflow_request.code_as_string,
            metadata=workflow_request.metadata,
            settings=workflow_request.settings,
            workflow_name=workflow_request.workflow_name,
        )

        # create unique name for lambda function
        function_name = generate_function_name(
            self.index_id, new_workflow.workflow_id, new_workflow.workflow_name
        )

        # check for code security and function
        code_handler = CodeHandler(
            self.index_id,
            new_workflow.workflow_id,
            new_workflow.code_as_string,
            function_name,
        )
        code_handler._validate_code()

        # upload to s3
        s3_dict = code_handler._create_zip_package(
            new_workflow.settings.requirements,
            new_workflow.settings.python_version,
        )["data"]

        # print(s3_dict)

        # create lambda function
        code_handler.create_lambda_function(s3_dict["bucket"], s3_dict["key"])

        new_workflow.metadata["serverless_function_name"] = function_name
        new_workflow.metadata["serverless_last_edited"] = current_time()

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

    @staticmethod
    def run(workflow, run_id, websocket_id, request_parameters):
        response_object = {
            "response": None,
            "error": None,
            "status": 500,
            "metadata": {},
        }
        try:
            print("Running function!")
            response = code_handler.run(request_parameters, workflow)
            response_object["response"] = response
        except Exception as e:
            response_object["error"] = f"Error running lambda: {e}"
            response_object["status"] = 500
