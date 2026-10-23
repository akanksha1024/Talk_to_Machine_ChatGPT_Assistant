"""Minimal ChatGPT API client implemented with requests, as required by the PDF."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

try:
    import requests
except ModuleNotFoundError:  # pragma: no cover - exercised only before setup
    requests = None

from .config import AppConfig


class ChatGPTAPIError(RuntimeError):
    """Raised when the API returns an error or an unexpected response."""


def sanitize_api_error(text: str) -> str:
    """Mask API keys that may be repeated inside provider error messages."""

    import re

    text = re.sub(r"sk-proj-[A-Za-z0-9_\-]+", "sk-proj-***MASKED***", text)
    text = re.sub(r"sk-[A-Za-z0-9_\-]+", "sk-***MASKED***", text)
    text = re.sub(r"snorkel_[A-Za-z0-9_\-]+", "snorkel_***MASKED***", text)
    return text


def format_api_error(status_code: int, response_text: str) -> str:
    """Return a clear, student-friendly API error message."""

    safe_text = sanitize_api_error(response_text)

    if "credit_balance_exhausted" in safe_text or "insufficient_quota" in safe_text:
        return (
            f"API request failed with status {status_code}: Your OpenAI API key is valid, "
            "but the account has no API credits remaining. Add credits in OpenAI billing, "
            "or run this project in demo mode with: python main.py --demo"
        )

    if "invalid_api_key" in safe_text:
        return (
            f"API request failed with status {status_code}: The API key is invalid. "
            "Create a valid key at https://platform.openai.com/api-keys and update .env."
        )

    if "model_not_found" in safe_text:
        return (
            f"API request failed with status {status_code}: The configured model is not "
            "available for this API key. Try a model listed in your OpenAI dashboard."
        )

    return f"API request failed with status {status_code}: {safe_text}"


@dataclass
class CompletionResponse:
    """Structured response returned by the assistant client."""

    text: str
    raw: dict[str, Any]


class OpenAICompletionClient:
    """Client for the completions endpoint shown in the project statement."""

    def __init__(self, config: AppConfig, timeout: int = 60) -> None:
        self.config = config
        self.timeout = timeout

    def build_headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}",
        }

    def build_payload(self, prompt: str) -> dict[str, Any]:
        return {
            "model": self.config.model,
            "prompt": prompt,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }

    def complete(self, prompt: str) -> CompletionResponse:
        clean_prompt = prompt.strip()
        if not clean_prompt:
            raise ValueError("Prompt cannot be empty.")

        if requests is None:
            raise ChatGPTAPIError(
                "The 'requests' package is not installed. Run: pip install -r requirements.txt"
            )

        response = requests.post(
            self.config.endpoint,
            headers=self.build_headers(),
            json=self.build_payload(clean_prompt),
            timeout=self.timeout,
        )

        if response.status_code != 200:
            raise ChatGPTAPIError(format_api_error(response.status_code, response.text))

        try:
            data = response.json()
            text = data["choices"][0]["text"].strip()
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise ChatGPTAPIError("API response did not contain choices[0].text.") from exc

        return CompletionResponse(text=text, raw=data)
