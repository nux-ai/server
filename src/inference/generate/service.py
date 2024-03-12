from model import Model
from utilities.methods import BadRequestError
import time
from typing import List

from .plugins.openai import GPT

"""
Blockers
- How to structure the classes?
    - do we need a generate_orchestrator, generate_handler, model_handler?
- How to structure ModelHandler?
    - do we need to support more than GPT off the bat?
    - which granularity to support? gpt vs gpt-3.5-turbo, etc
- 
"""


class ModelHandler:
    def __init__(self):
        self.model_classes = {
            "gpt": GPT,
        }

    async def execute(
        self,
        model_class,
    ):
        if model_class in self.model_classes:

            model_handler_class = self.model_classes[model_class](
                self.index_id,
                self.run_id,
            )
            async with model_handler_class as instance:
                return await instance.run()
        else:
            raise BadRequestError(f"Model class {model_class} not found")


class GenerateHandler:
    """
    GenerateHandler initializes model with json_enforcer and executes
    """

    def __init__(
        self,
        model,
        response_format,
        context,
        messages,
        settings,
    ):
        self.model = model
        self.response_format = response_format
        self.context = context
        self.messages = messages
        self.settings = settings

        self.model_handler = ModelHandler(
            self.model,
        )

    async def execute(self):

        return await self.model_handler.execute()


async def generate_orchestrator(
    model: Model = {"model_type": "GPT", "model_version": "gpt-3.5-turbo"},
    response_format: dict = None,
    context: str = None,
    messages: List[dict] = [],
    settings: dict = None,
):

    generate_handler = GenerateHandler(
        model,
        response_format,
        context,
        messages,
        settings,
    )

    return await generate_handler.execute()
