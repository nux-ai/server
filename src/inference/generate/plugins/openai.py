from config import openai_key
import json
import httpx
import time
from utilities.methods import get_token_count


class GPT:
    def __init__(
        self,
        engine,
        context,
        messages,
        settings,
    ):
        self.engine = engine
        self.context = context
        self.messages = messages
        self.settings = settings
        self.url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {openai_key}",
            "Content-Type": "application/json",
        }

    def _validate_gpt_input(self, input_tokens, parsed_settings):
        if "max_tokens" in parsed_settings:
            if input_tokens > parsed_settings["max_tokens"]:
                raise ValueError(
                    f"GPT input exceeds max_tokens of {parsed_settings['max_tokens']}, tokens provided: {input_tokens}."
                )

    async def run(self):
        # parse the settings
        parsed_settings = self._parse_settings(self.db_block["settings"])
        system_prompt = parsed_settings.pop("system_prompt", "")

        # parse the input
        parsed_input = self._parse_gpt_inputs()

        # validate the input
        input_tokens = get_token_count(parsed_settings["model"], parsed_input)

        # set it up
        system_object = {"role": "system", "content": ""}

        # prepare payload
        payload = {
            "messages": [{"role": "user", "content": parsed_input}, system_object],
            **parsed_settings,
        }

        print(json.dumps(payload, indent=4))

        if len(system_prompt) > 0:
            system_object["content"] += f" | {system_prompt}"

        print("calling chatgpt with user prompt")
        start_time = time.time() * 1000

        response_object = {
            "response": None,
            "error": None,
            "status": 500,
            "metadata": {},
        }

        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(
                    self.url, headers=self.headers, data=json.dumps(payload), timeout=60
                )

            gpt_response = r.json()

        except Exception as e:
            response_object["error"] = gpt_response["error"]
            response_object["status"] = 500

        response_object["metadata"] = {
            "runtime": (time.time() * 1000) - start_time,
            "output_token_count": gpt_response.get("usage", {}).get("total_tokens", 0),
            "input_token_count": input_tokens,
            "content_type": "application/json",
        }

        return response_object
