from openai import OpenAI

from datacamp_ai_engineering.provider_config import get_provider_settings

settings = get_provider_settings("gemini")
client = OpenAI(base_url=settings.base_url, api_key=settings.api_key)
for m in client.models.list().data:
    print(m.id)
