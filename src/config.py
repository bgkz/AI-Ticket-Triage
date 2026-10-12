import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


BASE_URL = "http://127.0.0.1:8000"
BASE_TIMEOUT_SEC = 20
API_KEY = os.getenv("API_KEY")
OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")
INVALID_OPENAI_KEY = os.getenv("INVALID_OPENAI_KEY")


if not API_KEY:
    raise RuntimeError("API_KEY missing")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY missing")
