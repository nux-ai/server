from openai import OpenAI
import instructor
from config import openai_key
import time
# from utilities.methods import get_token_count


client = instructor.patch(OpenAI(api_key=openai_key))


class GPT:
    def __init__(self, model, response_format, context, messages, settings):
        self.model = model
        self.response_format = response_format
        self.context = context
        self.messages = messages
        self.settings = settings

    async def run(self):
        # parse and validate settings
        # parse and validate context & messages

        print("calling chatgpt with user prompt")
        start_time = time.time() * 1000

        response_object = {
            "response": None,
            "error": None,
            "status": 500,
            "metadata": {},
        }

        try:
            completion = client.chat.completions.create(
                model=self.model.model_version,
                response_model=self.response_format,
                messages=self.messages,
            )

            response_object["response"] = completion

        except Exception as e:
            response_object["error"] = e
            response_object["status"] = 500

        response_object["metadata"] = {
            "runtime": (time.time() * 1000) - start_time,
            "output_token_count": response_object.get("usage", {}).get("total_tokens", 0),
            # "input_token_count": input_tokens,
            "content_type": "application/json",
        }

        return response_object
