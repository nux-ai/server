import traceback
from fastapi import HTTPException
import logging
import sentry_sdk
import tiktoken
import uuid


class BadRequestError(HTTPException):
    # deafults to 400 error if no error_code provided
    def __init__(self, detail=None, status_code=400, headers=None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


def log_and_send_to_sentry(e):
    logging.error("An error occurred: %s", e)
    traceback.print_exc()
    sentry_sdk.capture_exception(e)


def get_token_count(model_name, string):
    """Returns the number of tokens in a text string."""
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    num_tokens = len(encoding.encode(string))
    return num_tokens


def generate_uuid(length=36, dashes=True):
    x = uuid.uuid4()
    if dashes:
        return str(x)[:length]
    else:
        return str(x).replace("-", "")[:length]
