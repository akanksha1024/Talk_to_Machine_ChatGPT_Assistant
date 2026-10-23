import unittest
from unittest.mock import Mock, patch

from src.config import AppConfig
from src.openai_client import (
    ChatGPTAPIError,
    OpenAICompletionClient,
    format_api_error,
    sanitize_api_error,
)


class OpenAICompletionClientTests(unittest.TestCase):
    def setUp(self):
        self.config = AppConfig(api_key="test-key")
        self.client = OpenAICompletionClient(self.config)

    def test_build_headers_contains_json_and_bearer_token(self):
        headers = self.client.build_headers()
        self.assertEqual(headers["Content-Type"], "application/json")
        self.assertEqual(headers["Authorization"], "Bearer test-key")

    def test_build_payload_matches_project_statement_fields(self):
        payload = self.client.build_payload("Who invented ChatGPT?")
        self.assertEqual(payload["model"], "gpt-3.5-turbo-instruct")
        self.assertEqual(payload["prompt"], "Who invented ChatGPT?")
        self.assertEqual(payload["temperature"], 0.0)
        self.assertEqual(payload["max_tokens"], 100)

    @patch("src.openai_client.requests.post")
    def test_complete_returns_first_choice_text(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"choices": [{"text": "OpenAI created ChatGPT."}]}
        mock_post.return_value = mock_response

        result = self.client.complete("Who invented ChatGPT?")

        self.assertEqual(result.text, "OpenAI created ChatGPT.")
        mock_post.assert_called_once()

    @patch("src.openai_client.requests.post")
    def test_complete_raises_api_error_on_non_200(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_post.return_value = mock_response

        with self.assertRaises(ChatGPTAPIError):
            self.client.complete("Hello")

    def test_sanitize_api_error_masks_key_like_values(self):
        text = "Incorrect API key provided: snorkel_abc123 and sk-proj-secret123"
        sanitized = sanitize_api_error(text)
        self.assertNotIn("snorkel_abc123", sanitized)
        self.assertNotIn("sk-proj-secret123", sanitized)

    def test_format_api_error_explains_credit_exhaustion(self):
        text = '{"error": {"code": "credit_balance_exhausted"}}'
        formatted = format_api_error(429, text)
        self.assertIn("no API credits remaining", formatted)
        self.assertIn("--demo", formatted)


if __name__ == "__main__":
    unittest.main()
