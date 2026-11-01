import os
from typing import Any
from pprint import pprint
from dotenv import load_dotenv
from openai import (
    OpenAI,
    AuthenticationError,
    RateLimitError,
    APIConnectionError,
    APIStatusError,
)

from openai.types.chat.chat_completion import ChatCompletion

load_dotenv()

BASE_URL: str = "https://ollama.com/v1"
API_KEY: str = os.environ["OLLAMA_API_KEY"]
MODEL: str = os.environ["OLLAMA_MODEL_NAME"]


def get_response_from_ai(input_message: str) -> ChatCompletion | None:
    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
    try:
        response: ChatCompletion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": input_message,
                },
            ],
            max_completion_tokens=500,
        )
        return response
    except AuthenticationError as e:
        print(
            f"Authentication Error: message - {e.message}, status_code - {e.status_code}"  # noqa
        )
    except RateLimitError as e:
        print(
            f"Rate Limit Error Error: message - {e.message}, status_code - {e.status_code}"  # noqa
        )
    except APIConnectionError as e:
        print(
            f"API Connection Error: message - {e.message}, status_code - {e.status_code}"  # noqa
        )
    except APIStatusError as e:
        print(
            f"API Status Error: message - {e.message}, status_code - {e.status_code}"  # noqa
        )


def get_required_ai_response_data(
    response: ChatCompletion | None,
) -> tuple[str, dict[str, Any]]:
    if response:
        response_message: str = response.choices[0].message.content
        additional_data: dict = {
            "response_id": response.id,
            "model_name": response.model,
            "usage": response.usage,
            "finish_reason": response.choices[0].finish_reason,
        }
        return (response_message, additional_data)
    return ("", {})


def main():
    input_message = input("Enter your prompt: ")
    response = get_response_from_ai(input_message)
    message, additional_data = get_required_ai_response_data(response)
    print(f"{message}\n")
    pprint(additional_data)


if __name__ == "__main__":
    main()
