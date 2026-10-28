import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# BASE_URL: str = "https://ollama.com/v1"
BASE_URL: str = "https://api.groq.com/openai/v1"
API_KEY: str = os.environ["GROQ_API_KEY"]

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

model_list = client.models.list().data
for model in model_list:
    print(model.id)
