import os
from typing import Any
from pprint import pprint
from dotenv import load_dotenv
from openai import OpenAI

from openai.types import CompletionUsage
from openai.types.chat.chat_completion import ChatCompletion, Choice

load_dotenv()

BASE_URL: str = os.environ["OLLAMA_BASE_URL"]
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
            max_completion_tokens=2000,
            temperature=0,
        )
        return response
    except Exception as e:
        print(e)


def get_required_ai_response_data(
    response: ChatCompletion | None,
) -> tuple[str, dict[str, Any]]:
    total_tokens: int = 0
    response_message: str = ""
    if response:
        choice_data_list: list[Choice] = response.choices
        choice_data_first: Choice = choice_data_list[0]
        usage_data: CompletionUsage | None = response.usage
        if choice_data_first.message.content:
            response_message = choice_data_first.message.content
        if usage_data is not None:
            total_tokens = usage_data.total_tokens
        additional_data: dict = {
            "response_id": response.id,
            "model_name": response.model,
            "total_tokens": total_tokens,
            "finish_reason": choice_data_first.finish_reason,
        }
        return (response_message, additional_data)
    return ("", {})


def main():
    input_message = """
        Objective:
            - Replace every reference to a car with an airplane.
            - Adjust the surrounding sentences so that the resulting
            paragraph is factually appropriate.
        Data:
            A car is a vehicle that is typically powered by an
            internal combustion engine or an electric motor.
            It has four wheels and is designed to carry passengers
            or cargo on roads.
    """
    response = get_response_from_ai(input_message)
    message, additional_data = get_required_ai_response_data(response)
    print(f"{message}\n")
    pprint(additional_data)


if __name__ == "__main__":
    main()
