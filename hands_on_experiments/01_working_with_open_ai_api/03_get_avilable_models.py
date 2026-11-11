from openai import OpenAI

from datacamp_ai_engineering.provider_config import get_provider_settings

# Select which provider's compatible model list to inspect.
# PROVIDER = "ollama"
PROVIDER = "groq"
# PROVIDER = "gemini"
settings = get_provider_settings(PROVIDER)
client = OpenAI(base_url=settings.base_url, api_key=settings.api_key)

model_list = client.models.list().data
for model in model_list:
    print(model.id)
