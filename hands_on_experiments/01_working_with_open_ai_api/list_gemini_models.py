import os
import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError('Set GEMINI_API_KEY')
url = f"{BASE_URL}/models?key={API_KEY}"
resp = requests.get(url)
print('status', resp.status_code)
print(resp.text)
