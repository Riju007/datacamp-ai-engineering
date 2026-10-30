import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(verbose=True)
API_KEY = os.getenv("OLLAMA_API_KEY", "ollama")
# API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = "http://localhost:11434/v1"

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

start = time.perf_counter()
response = client.chat.completions.create(
    model="lfm2.5-thinking:1.2b",
    # model="phi4-mini:latest",
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
print(f"{elapsed:.2f}s {tokens=} {tokens / elapsed:.1f} tokens/sec")

print("-------")

print(response.choices[0].message.content)
