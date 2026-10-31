import os

# from typing import Any
# from pprint import pprint
from dotenv import load_dotenv
from openai import OpenAI

# from openai.types import CompletionUsage
from openai.types.chat.chat_completion import ChatCompletion, Choice

load_dotenv()

BASE_URL: str = os.environ["OLLAMA_BASE_URL"]
API_KEY: str = os.environ["OLLAMA_API_KEY"]
MODEL: str = os.environ["OLLAMA_MODEL_NAME"]

client: OpenAI = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def get_response_form_ai(
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


def summarize_text(text: str, bullet_points: int) -> str:
    if bullet_points <= 0:
        raise ValueError("Bullet points must be greater than zero")
    prompt = f"""
    Your Role: You are an expert in summarize things and getting the key data.
    Objective:
        - summarize the below data
        - make it clear concise and crisp
        - summarize content should be easy and clear to understand
    Constraint:
        - Use only information present in the source text.
        - Preserve all numerical values accurately.
        - If information is missing, do not infer it.
    Output format:
        - Return exactly {bullet_points} bullet points.
        - Do not include headings.
        - Each bullet should contain one key finding.
    Example:
        1. This is point 1.
        2. This is point 2.
        ...
        n. This is point n.
    content: {text}
    """
    response = get_response_form_ai(client, prompt)
    response_message: str = ""
    choice_data_list: list[Choice] = []
    if response:
        choice_data_list = response.choices
        if len(choice_data_list) > 0:
            choice_data_first: Choice = choice_data_list[0]
            if choice_data_first.message.content:
                response_message = choice_data_first.message.content
    return response_message


def main():
    finance_text = """
        The company reported revenue of $10 million during Q1,
        representing a 15% increase compared to the previous quarter.
        Operating expenses increased by 8%, primarily due to
        higher infrastructure and employee costs.

        The company expanded into three new markets and acquired
        2,000 new customers. Customer retention improved from
        85% to 91%.

        Management expects revenue growth of 20% in the next quarter,
        although increased competition and economic uncertainty
        remain potential challenges.
    """
    summarized_text_data: str = summarize_text(finance_text, 5)
    print(summarized_text_data)


if __name__ == "__main__":
    main()
