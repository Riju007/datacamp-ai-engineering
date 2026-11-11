from openai import OpenAI

from datacamp_ai_engineering.provider_config import get_provider_settings

settings = get_provider_settings("ollama")

client = OpenAI(base_url=settings.base_url, api_key=settings.api_key)
response = client.chat.completions.create(
    model=settings.model,
    messages=[
        {
            "role": "user",
            "content": "Write a polite reply accepting an AI Engineer job offer."  # noqa
        }
    ]
)
print(response.choices[0].message.content)
