"""Shared environment configuration for the provider examples."""

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(ENV_FILE, override=False)


@dataclass(frozen=True)
class ProviderSettings:
    api_key: str
    base_url: str
    model: str
    native_base_url: str | None = None


_PROVIDER_DEFAULTS = {
    "groq": {
        "api_key": "GROQ_API_KEY",
        "base_url_env": "GROQ_BASE_URL",
        "base_url": "https://api.groq.com/openai/v1",
        "model_env": "GROQ_MODEL_NAME",
        "model": "openai/gpt-oss-120b",
    },
    "ollama": {
        "api_key": "OLLAMA_API_KEY",
        "base_url_env": "OLLAMA_BASE_URL",
        "base_url": "https://ollama.com/v1",
        "model_env": "OLLAMA_MODEL_NAME",
        "model": "gpt-oss:120b",
    },
    "gemini": {
        "api_key": "GEMINI_API_KEY",
        "base_url_env": "GEMINI_BASE_URL",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "model_env": "GEMINI_MODEL_NAME",
        "model": "gemini-2.5-flash",
    },
}


def get_provider_settings(
    provider: str,
    *,
    base_url: str | None = None,
    model: str | None = None,
) -> ProviderSettings:
    """Return settings for a provider, using the root .env and shell values."""
    provider_name = provider.lower()
    if provider_name not in _PROVIDER_DEFAULTS:
        supported = ", ".join(sorted(_PROVIDER_DEFAULTS))
        raise ValueError(
            f"Unknown provider {provider!r}. Choose from: {supported}."
        )

    defaults = _PROVIDER_DEFAULTS[provider_name]
    resolved_base_url = (
        base_url or os.getenv(defaults["base_url_env"]) or defaults["base_url"]
    )
    api_key = os.getenv(defaults["api_key"])

    if not api_key and provider_name == "ollama":
        hostname = urlparse(resolved_base_url).hostname
        if hostname in {"localhost", "127.0.0.1", "::1"}:
            api_key = "ollama"

    if not api_key:
        raise RuntimeError(
            f"Missing {defaults['api_key']}. "
            "Set it in the root .env file or shell."
        )

    native_base_url = None
    if provider_name == "gemini":
        native_base_url = os.getenv(
            "GEMINI_API_BASE_URL",
            "https://generativelanguage.googleapis.com/v1beta",
        )

    return ProviderSettings(
        api_key=api_key,
        base_url=resolved_base_url,
        model=model or os.getenv(defaults["model_env"]) or defaults["model"],
        native_base_url=native_base_url,
    )
