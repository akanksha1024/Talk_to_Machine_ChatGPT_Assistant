# Talk to Machines: Build AI Assistants with ChatGPT

This is the  project , It implements a Python chatbot that communicates with the ChatGPT API using `requests`.

## Project Contents

- `main.py` - application entry point.
- `src/config.py` - API key and runtime configuration.
- `src/openai_client.py` - API request/response logic.
- `src/chatbot.py` - interactive chatbot loop and transcript saving.
- `tests/` - unit tests for payloads, headers, and chatbot helpers.
- `docs/PROJECT_REPORT.md` - college-style project report.
- `.env.example` - safe example for API key setup.
- `sample_output.txt` - sample interaction.

## Setup

1. Install Python 3.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file from the example:

```bash
cp .env.example .env
```

4. Replace the placeholder API key in `.env`:

```text
OPENAI_API_KEY=<your_api_key_here>
```

## Run the Chatbot

```bash
python3 main.py
```

Type a message and press Enter. Type `exit` or `quit` to stop.

## Demo Mode

Use demo mode if you want to show the interface without using an API key:

```bash
python3 main.py --demo
```

## Run Tests

```bash
python3 -m unittest discover -s tests
```

## Troubleshooting

- `No module named requests`: run `python3 -m pip install -r requirements.txt`.
- `invalid_api_key`: update `.env` with a valid OpenAI API key from `https://platform.openai.com/api-keys`.
- `credit_balance_exhausted`: the API key is valid, but the account has no API credits. Add credits in OpenAI billing or run `python3 main.py --demo`.
- If your Mac has another global `OPENAI_API_KEY`, this project uses the local `.env` file first so unrelated keys do not affect the project.

## Notes

The project follows the PDF instructions by using:

- `requests`
- API key authentication
- `https://api.openai.com/v1/completions`
- JSON payload with model, prompt, temperature, and max tokens
- POST request handling
- continuous interactive input loop

Do not submit a real `.env` file containing your API key.
