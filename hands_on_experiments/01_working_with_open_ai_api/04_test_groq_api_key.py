import time

from openai import OpenAI

from datacamp_ai_engineering.provider_config import get_provider_settings

settings = get_provider_settings("groq")
client = OpenAI(base_url=settings.base_url, api_key=settings.api_key)

# for model in client.models.list().data:
#     print(model.id)

start = time.perf_counter()
response = client.chat.completions.create(
    model=settings.model,  # no "-cloud" suffix when calling directly
    # model="whisper-large-v3-turbo",
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
