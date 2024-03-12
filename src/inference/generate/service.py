from .models.IModel import IModel
from .models.model import GenerationRequest, GenerationResponse

from .plugins.openai import GPT


class ModelHandler:
    @staticmethod
    def model_factory(type, *args, **kwargs) -> IModel:
        if type.lower() == "gpt":
            return GPT(*args, **kwargs)
        # TODO: Add other model types like LLaMA, etc
        else:
            raise ValueError(f"Unsupported model type: {type}")


async def generate_orchestrator(request: GenerationRequest) -> GenerationResponse:
    model_instance: IModel = ModelHandler.model_factory(
        request.model.type,
        request,
    )
    return model_instance.run()
