# Talk to Machines: Build AI Assistants with ChatGPT

## Project Description

This project builds a real-time conversational AI assistant using Python and the ChatGPT API. The assistant accepts natural-language user input, sends a structured prompt to the API, receives the model response, and displays it in an interactive terminal chat interface.

## Problem Statement

Conversational AI is useful in customer support, education, productivity tools, and virtual assistants. Developers need to understand API communication, authentication, prompt construction, response handling, and interactive chatbot design. This project demonstrates those skills through a Python-based implementation.

## Objectives

- Connect Python code with the ChatGPT API.
- Authenticate securely with an API key.
- Send structured JSON payloads to the API.
- Process successful responses and error responses.
- Provide a continuous input loop for real-time conversation.
- Save a transcript for review or demonstration.

## Tools and Technologies

- Python 3
- `requests` library
- OpenAI completions endpoint
- Environment variable based API key handling
- Unit tests using Python `unittest`

## System Workflow

1. The user starts the application from the terminal.
2. The program loads the API key from the environment or `.env`.
3. The user enters a question or message.
4. The application builds a structured prompt.
5. The application sends a POST request to the API endpoint with headers and JSON data.
6. If the response is successful, the assistant prints the model answer.
7. If the response fails, the assistant prints a readable error.
8. The conversation continues until the user types `exit` or `quit`.
9. A transcript is saved as `chat_transcript.txt`.

## API Request Design

Endpoint:

```text
https://api.openai.com/v1/completions
```

Headers:

```python
{
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
```

Payload:

```python
{
    "model": "gpt-3.5-turbo-instruct",
    "prompt": "User question",
    "temperature": 0,
    "max_tokens": 100
}
```

## Features

- Interactive chatbot interface.
- API key kept outside source code.
- Configurable model, temperature, and maximum token count.
- Structured prompt builder.
- Error handling for failed API requests.
- Offline demo mode for presentation without exposing an API key.
- Transcript generation.
- Unit tests for payload, headers, success response, and error response.

## Security Considerations

The API key is not hardcoded in the final program. It should be provided through an environment variable or a private `.env` file. The `.env` file is ignored by Git and should not be submitted publicly.

## Conclusion

The project successfully demonstrates how to build a Python chatbot using the ChatGPT API. It covers authentication, request creation, response handling, interactive conversation, and basic software quality practices such as modular code and tests.
