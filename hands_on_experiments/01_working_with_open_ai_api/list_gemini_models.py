import requests

from datacamp_ai_engineering.provider_config import get_provider_settings

settings = get_provider_settings("gemini")
BASE_URL = settings.native_base_url or settings.base_url
API_KEY = settings.api_key
url = f"{BASE_URL}/models?key={API_KEY}"
resp = requests.get(url)
print('status', resp.status_code)
print(resp.text)
