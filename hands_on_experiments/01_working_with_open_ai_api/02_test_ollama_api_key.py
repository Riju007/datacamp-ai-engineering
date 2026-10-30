import os
import time

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://ollama.com/v1"

API_KEY = os.environ["OLLAMA_API_KEY"]

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# for model in client.models.list().data:
#     print(model.id)

start = time.perf_counter()
response = client.chat.completions.create(
    model="gpt-oss:120b",  # no "-cloud" suffix when calling directly
    messages=[
        {
            "role": "user",
            "content": "In 3 bullet points, future of Rust in AI.",
        }
    ],
    max_tokens=1000,
)
elapsed = time.perf_counter() - start
tokens = response.usage.completion_tokens
print(f"{elapsed:.2f}s {tokens=} {tokens/elapsed:.1f} tokens/sec")
print("-------")
print(response.choices[0].message.content)
