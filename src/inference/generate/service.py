from fastapi import HTTPException

from generate.models.IModel import IModel
from generate.models.model import GenerationRequest, GenerationResponse

from generate.plugins.openai import GPT


class ModelHandler:
    @staticmethod
    def model_factory(provider, *args, **kwargs) -> IModel:
        if provider.lower() == "gpt":
            return GPT(*args, **kwargs)
        # TODO: Add other model types like LLaMA, etc
        else:
            raise ValueError(f"Unsupported model provider: {provider}")


async def generate_orchestrator(request: GenerationRequest) -> GenerationResponse:
    try:
        model_instance: IModel = ModelHandler.model_factory(
            request.model.provider,
            request,
        )
        return model_instance.run()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
