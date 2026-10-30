import os
import time
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY in .env")

# Use the pure HTTP interface (requests) – the OpenAI client sends a bearer token
# which Gemini does not accept.  The API key is supplied via the ``key`` query
# parameter.

def list_gemini_models():
    """Return the list of available Gemini models.

    The endpoint ``GET {BASE_URL}/models`` returns a JSON object with a ``models``
    array.  We surface the raw JSON for debugging.
    """
    url = f"{BASE_URL}/models?key={API_KEY}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def gemini_generate(model, instructions, input_, max_output_tokens=500):
    """Call Gemini's ``generateContent`` endpoint via ``requests``.

    Returns the parsed JSON response.
    """
    url = f"{BASE_URL}/models/{model}:generateContent?key={API_KEY}"
    payload = {
        "systemInstruction": {"parts": [{"text": instructions}]},
        "contents": [{"role": "user", "parts": [{"text": input_}]}],
        "generationConfig": {"maxOutputTokens": max_output_tokens},
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()


# First, discover a model that supports generateContent
models_info = list_gemini_models()
# Find the first model name – in practice you would filter for the desired model.
# Pick the first model name and strip any leading "models/" prefix
raw_name = models_info.get("models", [{}])[0].get("name", "gemini-1.5-flash")
model_name = raw_name.split("/")[-1]  # e.g. "gemini-2.5-flash"

start = time.perf_counter()
resp = gemini_generate(
    model=model_name,
    instructions="You are a tech expert who can see future trends.",
    input_="In 3 bullet points, future of Rust in AI.",
)
elapsed = time.perf_counter() - start

# Retrieve token usage information in a tolerant way – the exact key name can
# vary between Gemini's raw response ("usageMetadata") and the OpenAI-compatible
# wrapper ("usage"). We fall back to an empty dict if neither is present.
usage_info = resp.get("usageMetadata") or resp.get("usage") or {}
# The total token count may be under different field names depending on the API version.
total_tokens = (
    usage_info.get("totalTokenCount")
    or usage_info.get("total_tokens")
    or usage_info.get("totalTokens")
    or 0
)
print(f"{elapsed:.2f}s tokens={total_tokens}")
print("-------")
# Debug: show full response structure to understand available keys
print("FULL RESPONSE:", resp)
# Attempt to print the generated text if the expected structure is present
if isinstance(resp, dict) and "candidates" in resp:
    print(resp["candidates"][0]["content"]["parts"][0]["text"])
else:
    # Fallback: try common alternative keys
    for key in ("candidates", "responses", "output_text"):
        if key in resp:
            print(f"{key} found but unexpected shape: {resp[key]}")
            break
    else:
        print("Unable to locate generated text in response.")