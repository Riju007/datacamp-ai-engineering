import os
import unittest
from pathlib import Path
from unittest.mock import patch

from datacamp_ai_engineering.provider_config import (
    ENV_FILE,
    PROJECT_ROOT,
    get_provider_settings,
)


class ProviderSettingsTests(unittest.TestCase):
    def test_env_file_is_resolved_from_project_root(self):
        self.assertEqual(ENV_FILE, PROJECT_ROOT / ".env")
        self.assertEqual(PROJECT_ROOT, Path(__file__).resolve().parents[1])

    def test_groq_settings_use_environment_values(self):
        with patch.dict(
            os.environ,
            {
                "GROQ_API_KEY": "test-key",
                "GROQ_BASE_URL": "https://example.test/v1",
                "GROQ_MODEL_NAME": "test-model",
            },
            clear=True,
        ):
            settings = get_provider_settings("groq")

        self.assertEqual(settings.api_key, "test-key")
        self.assertEqual(settings.base_url, "https://example.test/v1")
        self.assertEqual(settings.model, "test-model")

    def test_local_ollama_uses_placeholder_key_and_explicit_model(self):
        with patch.dict(os.environ, {}, clear=True):
            settings = get_provider_settings(
                "ollama",
                base_url="http://localhost:11434/v1",
                model="test-model",
            )

        self.assertEqual(settings.api_key, "ollama")
        self.assertEqual(settings.model, "test-model")

    def test_gemini_native_endpoint_is_available(self):
        with patch.dict(
            os.environ, {"GEMINI_API_KEY": "test-key"}, clear=True
        ):
            settings = get_provider_settings("gemini")

        self.assertEqual(
            settings.native_base_url,
            "https://generativelanguage.googleapis.com/v1beta",
        )

    def test_missing_api_key_has_actionable_error(self):
        with patch.dict(os.environ, {}, clear=True), self.assertRaisesRegex(
            RuntimeError, "GROQ_API_KEY"
        ):
            get_provider_settings("groq")


if __name__ == "__main__":
    unittest.main()
