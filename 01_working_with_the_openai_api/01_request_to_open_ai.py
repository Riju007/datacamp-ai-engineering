import os
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

BASE_URL = "https://ollama.com/v1"
API_KEY = os.environ["OLLAMA_API_KEY"]

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
response = client.chat.completions.create(
    model="gpt-oss:120b",
    messages=[
        {
            "role": "user",
            "content": "Write a polite reply accepting an AI Engineer job offer."  # noqa
        }
    ]
)
print(response.choices[0].message.content)
