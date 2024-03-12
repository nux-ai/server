from models.IModel import IModel
from models.model import GenerationResponse

from .plugins.openai import GPT


class ModelHandler:
    @staticmethod
    def model_factory(model_type, *args, **kwargs) -> IModel:
        if model_type.lower() == "gpt":
            return GPT(*args, **kwargs)
        # Add elif for other model types like LLaMA
        else:
            raise ValueError(f"Unsupported model type: {model_type}")


async def generate_orchestrator(request) -> GenerationResponse:
    model_instance: IModel = ModelHandler.model_factory(
        request.model.model_type,
        request.model,
        request.response_format,
        request.context,
        request.messages,
        request.settings,
    )
    return await model_instance.run()
