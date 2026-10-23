import unittest

from src.chatbot import build_prompt, demo_response


class ChatbotTests(unittest.TestCase):
    def test_build_prompt_wraps_user_input(self):
        prompt = build_prompt("Explain prompt engineering.")
        self.assertIn("User: Explain prompt engineering.", prompt)
        self.assertTrue(prompt.endswith("Assistant:"))

    def test_demo_response_is_available_without_api_key(self):
        response = demo_response("Hello")
        self.assertIn("Demo mode response", response)


if __name__ == "__main__":
    unittest.main()
