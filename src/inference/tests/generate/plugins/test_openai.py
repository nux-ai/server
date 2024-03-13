import pytest
from fastapi import HTTPException
from unittest.mock import patch, MagicMock
from generate.plugins.openai import GPT
from generate.models.model import GenerationRequest, GenerationResponse


@pytest.fixture
def generation_request():
    # Mock a GenerationRequest object with necessary attributes for testing
    return GenerationRequest(
        model={"provider": "gpt", "model": "gpt-3.5-turbo"}, settings={}, messages=[]
    )


@pytest.fixture
def gpt_instance(generation_request):
    # Instantiate the GPT class with a mocked GenerationRequest
    return GPT(generation_request)


def test_init(gpt_instance, generation_request):
    assert (
        gpt_instance.generation_request is generation_request
    ), "Initialization failed to correctly assign generation_request"


def test_extract_settings(gpt_instance):
    # Assuming settings is a dict in GenerationRequest, modify as necessary
    gpt_instance.generation_request.settings = {
        "test_setting": "value",
        "system_prompt": "ignore_this",
    }
    settings = gpt_instance._extract_settings()
    assert settings == {
        "test_setting": "value"
    }, "Settings extraction did not work as expected"


def test_extract_response_format_success(gpt_instance):
    # Mock a simple JSON schema for testing
    gpt_instance.generation_request.response_format = {
        "type": "object",
        "properties": {"name": {"type": "string"}},
    }
    model_class = gpt_instance._extract_response_format()
    assert model_class is not None, "Failed to parse JSON schema into a model class"


def test_extract_response_format_failure(gpt_instance):
    # Provide an invalid JSON schema
    gpt_instance.generation_request.response_format = {"invalid": "schema"}
    with pytest.raises(ValueError, match="JSON Schema parsing failed"):
        _ = gpt_instance._extract_response_format()


@patch("generate.plugins.openai.client.chat.completions.create")
def test_run_success(mock_completion_create, gpt_instance):
    # Setup mock return value
    mock_completion = MagicMock()
    mock_completion._raw_response = MagicMock(usage=MagicMock(total_tokens=123))
    mock_completion_create.return_value = mock_completion

    # Call the method
    response = gpt_instance.run()

    # Assertions to validate successful execution and response structure
    assert response.status == 200, "Expected status code 200 on success"
    assert isinstance(
        response, GenerationResponse
    ), "Response object is not of type GenerationResponse"
    assert mock_completion_create.called, "Expected completion.create to be called"


@patch(
    "generate.plugins.openai.client.chat.completions.create",
    side_effect=Exception("Test error"),
)
def test_run_failure(mock_completion_create, gpt_instance):
    # Test handling of exceptions
    with pytest.raises(HTTPException) as exc_info:
        _ = gpt_instance.run()
    assert exc_info.value.status_code == 500, "Expected HTTP 500 status code on error"
