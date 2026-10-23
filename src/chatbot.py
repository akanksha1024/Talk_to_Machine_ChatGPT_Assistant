"""Interactive chatbot application for the college project submission."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from .config import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    get_config,
)
from .openai_client import ChatGPTAPIError, OpenAICompletionClient


WELCOME_TEXT = """Talk to Machines: Build AI Assistants with ChatGPT
Type your message and press Enter. Type 'exit' or 'quit' to stop.
"""


def build_prompt(user_input: str) -> str:
    """Create a structured prompt while keeping the user message clear."""

    return (
        "You are a helpful, concise AI assistant. Answer the user's question clearly.\n\n"
        f"User: {user_input.strip()}\n"
        "Assistant:"
    )


def save_transcript(transcript: list[tuple[str, str]], output_path: Path) -> None:
    """Save a readable chat transcript for demonstration and review."""

    lines = [
        "Talk to Machines: ChatGPT Assistant Transcript",
        f"Generated at: {datetime.now().isoformat(timespec='seconds')}",
        "",
    ]
    for speaker, message in transcript:
        lines.append(f"{speaker}: {message}")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def demo_response(user_input: str) -> str:
    """Offline demo response used only when the presenter has no API key."""

    return (
        "Demo mode response: I received your message and would normally send it "
        "to the ChatGPT API using the configured endpoint, headers, and JSON payload."
    )


def run_interactive(client: OpenAICompletionClient | None, demo: bool) -> None:
    transcript: list[tuple[str, str]] = []
    print(WELCOME_TEXT)

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Bot: Goodbye.")
            break
        if not user_input:
            print("Bot: Please type a question or command.")
            continue

        prompt = build_prompt(user_input)
        transcript.append(("You", user_input))

        if demo:
            answer = demo_response(user_input)
        else:
            assert client is not None
            try:
                answer = client.complete(prompt).text
            except ChatGPTAPIError as exc:
                answer = f"Error: {exc}"
            except ValueError as exc:
                answer = f"Input error: {exc}"

        transcript.append(("Bot", answer))
        print(f"Bot: {answer}")

    if transcript:
        save_transcript(transcript, Path("chat_transcript.txt"))
        print("Transcript saved to chat_transcript.txt")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build AI Assistants with ChatGPT - interactive Python chatbot."
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Completion model to use. Default: {DEFAULT_MODEL}",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help="Creativity level from 0 to 2. Default: 0",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=DEFAULT_MAX_TOKENS,
        help="Maximum response length. Default: 100",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run without an API key using local demonstration responses.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.demo:
        run_interactive(client=None, demo=True)
        return

    config = get_config(
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )
    client = OpenAICompletionClient(config)
    run_interactive(client=client, demo=False)
