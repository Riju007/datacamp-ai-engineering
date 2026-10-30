import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
API_KEY = os.getenv("GEMINI_API_KEY")
client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
for m in client.models.list().data:
    print(m.id)
