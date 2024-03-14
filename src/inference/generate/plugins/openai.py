from openai import OpenAI, NotFoundError
import instructor
from config import openai_key
import json
import time

from generate.models.model import GenerationRequest, GenerationResponse
from _utils import generate_uuid, current_time
from _exceptions import (
    JSONSchemaParsingError,
    ModelExecutionError,
    UnsupportedModelVersionError,
)

from datamodel_code_generator import DataModelType, PythonVersion
from datamodel_code_generator.model import get_data_model_types
from datamodel_code_generator.parser.jsonschema import JsonSchemaParser


client = instructor.patch(OpenAI(api_key=openai_key))


class GPT:
    def __init__(self, generation_request: GenerationRequest):
        self.generation_request = generation_request

    def _extract_settings(self):
        if self.generation_request.settings:
            return {
                k: v
                for k, v in self.generation_request.settings.model_dump().items()
                if v is not None and k != "system_prompt"
            }
        return {}

    def _extract_response_format(self):
        if not self.generation_request.response_format:
            return None

        json_schema = json.dumps(self.generation_request.response_format)

        data_model_types = get_data_model_types(
            DataModelType.PydanticV2BaseModel,
            target_python_version=PythonVersion.PY_310,
        )
        parser = JsonSchemaParser(
            json_schema,
            data_model_type=data_model_types.data_model,
            data_model_root_type=data_model_types.root_model,
            data_model_field_type=data_model_types.field_model,
            data_type_manager_type=data_model_types.data_type_manager,
            dump_resolve_reference_action=data_model_types.dump_resolve_reference_action,
        )
        result = parser.parse()
        local_namespace = {}
        exec(result, globals(), local_namespace)
        model_class = local_namespace.get("Model")

        if model_class is None:
            raise JSONSchemaParsingError(f"JSON Schema parsing failed")

        return model_class

    def run(self):
        response_object = GenerationResponse(
            generation_id=generate_uuid(),
            created_at=current_time(),
            model=self.generation_request.model,
            metadata=None,
            response={},
            error=None,
            status=500,
            success=False,
        )

        settings = self._extract_settings()
        response_format = self._extract_response_format()

        if self.generation_request.context:
            self.generation_request.messages.append(
                {"role": "user", "content": self.generation_request.context}
            )

        try:
            start_time = time.time() * 1000
            completion = client.chat.completions.create(
                model=self.generation_request.model.model,
                response_model=response_format,
                messages=self.generation_request.messages,
                **settings,
            )

            response_object.response = completion
            response_object.metadata = {
                "elapsed_time": (time.time() * 1000) - start_time,
                "output_token_count": completion._raw_response.usage.total_tokens,
            }
            response_object.status = 200
            response_object.success = True
        except NotFoundError as e:
            raise UnsupportedModelVersionError()
        except Exception as e:
            raise ModelExecutionError()

        return response_object
