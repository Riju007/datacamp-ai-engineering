from typing import Final

from openai import OpenAI

# from openai.types import CompletionUsage
from openai.types import CompletionUsage
from openai.types.chat.chat_completion import ChatCompletion

from datacamp_ai_engineering.provider_config import get_provider_settings

settings = get_provider_settings("gemini")
BASE_URL: Final[str] = settings.base_url
API_KEY: Final[str] = settings.api_key
MODEL: Final[str] = settings.model

client: OpenAI = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def get_response_from_ai(
    client: OpenAI, input_message: str
) -> ChatCompletion | None:
    try:
        response: ChatCompletion = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": input_message}],
            max_completion_tokens=2300,
        )
        return response
    except Exception as e:
        print(e)


def calculate_api_cost(
    input_tokens: int,
    output_tokens: int,
    input_price: float,
    output_price: float,
) -> float:
    input_cost = (input_tokens / 1_000_000) * input_price
    output_cost = (output_tokens / 1_000_000) * output_price
    cost = input_cost + output_cost
    print(f"Input Cost: {input_cost:.8f}")
    print(f"Output Cost: {output_cost:.8f}")
    return cost


def main():
    prompt: str = "What is the capital of India?"
    api_cost: float = 0.00
    response = get_response_from_ai(client=client, input_message=prompt)
    # print(response.choices[0].message.content)
    if response is not None:
        usage: CompletionUsage | None = response.usage
        if usage is not None:
            api_cost = calculate_api_cost(
                input_tokens=usage.prompt_tokens,
                output_tokens=usage.completion_tokens,
                input_price=0.15,
                output_price=0.60,
            )
    print(f"Total Cost: {api_cost:.5f}")


if __name__ == "__main__":
    main()
