import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.config import get_config


class ConfigTests(unittest.TestCase):
    def test_project_dotenv_takes_priority_over_global_environment(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dotenv = Path(tmpdir) / ".env"
            dotenv.write_text("OPENAI_API_KEY=sk-proj-local-key\n", encoding="utf-8")

            with patch.dict(os.environ, {"OPENAI_API_KEY": "snorkel_wrong_key"}):
                old_cwd = os.getcwd()
                try:
                    os.chdir(tmpdir)
                    config = get_config()
                finally:
                    os.chdir(old_cwd)

        self.assertEqual(config.api_key, "sk-proj-local-key")


if __name__ == "__main__":
    unittest.main()
