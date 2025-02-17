import os

from dotenv import load_dotenv

load_dotenv()

# Discord Settings
AUTHORIZED_SERVER_IDS: list[int] = list(map(int, os.environ["AUTHORIZED_SERVER_IDS"].split(",")))
ADMIN_USER_IDS: list[int] = list(map(int, os.environ["ADMIN_USER_IDS"].split(",")))
MAX_CHARS_PER_RESPONSE: int = int(os.environ["MAX_CHARS_PER_RESPONSE"])

# OpenAI Settings
AVAILABLE_MODELS: list[str] = os.environ["AVAILABLE_MODELS"].split(",")
MAX_CONTEXT_WINDOW: int = int(os.environ["MAX_CONTEXT_WINDOW"])
MAX_TOKENS: int = int(os.environ["MAX_TOKENS"])
SEPARATOR_TOKEN: str = os.environ["SEPARATOR_TOKEN"]
TEMPERATURE: float = float(os.environ["TEMPERATURE"])
TOP_P: float = float(os.environ["TOP_P"])
