"""Configuration helpers for the ChatGPT assistant."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


DEFAULT_ENDPOINT = "https://api.openai.com/v1/completions"
DEFAULT_MODEL = "gpt-3.5-turbo-instruct"
DEFAULT_TEMPERATURE = 0.0
DEFAULT_MAX_TOKENS = 100


@dataclass(frozen=True)
class AppConfig:
    """Runtime settings for the assistant."""

    api_key: str
    endpoint: str = DEFAULT_ENDPOINT
    model: str = DEFAULT_MODEL
    temperature: float = DEFAULT_TEMPERATURE
    max_tokens: int = DEFAULT_MAX_TOKENS


def read_dotenv(path: str | Path = ".env") -> dict[str, str]:
    """Read simple KEY=VALUE pairs from a .env file without extra dependencies."""

    dotenv_path = Path(path)
    if not dotenv_path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        values[key] = value

    return values


def load_dotenv(path: str | Path = ".env", override: bool = False) -> None:
    """Load simple KEY=VALUE pairs into the process environment."""

    for key, value in read_dotenv(path).items():
        if override:
            os.environ[key] = value
        else:
            os.environ.setdefault(key, value)


def get_config(
    api_key: str | None = None,
    endpoint: str = DEFAULT_ENDPOINT,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> AppConfig:
    """Build validated configuration from arguments and environment variables."""

    dotenv_values = read_dotenv()
    resolved_key = (
        api_key
        or dotenv_values.get("OPENAI_API_KEY", "").strip()
        or os.getenv("OPENAI_API_KEY", "").strip()
    )
    if not resolved_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Add it to your environment or create a .env file."
        )

    if not endpoint.startswith("https://"):
        raise ValueError("The API endpoint must use HTTPS.")

    if max_tokens <= 0:
        raise ValueError("max_tokens must be greater than zero.")

    if not 0 <= temperature <= 2:
        raise ValueError("temperature must be between 0 and 2.")

    return AppConfig(
        api_key=resolved_key,
        endpoint=endpoint,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
