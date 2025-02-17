import os

from dotenv import load_dotenv

load_dotenv()

# ------ Discord Settings ------
AUTHORIZED_SERVER_IDS: list[int] = list(map(int, os.environ["AUTHORIZED_SERVER_IDS"].split(",")))
ADMIN_USER_IDS: list[int] = list(map(int, os.environ["ADMIN_USER_IDS"].split(",")))
BOT_NAME: str = os.environ["BOT_NAME"]
MAX_CHARS_PER_RESPONSE: int = int(os.environ["MAX_CHARS_PER_RESPONSE"])
# ------------------------------

# ------ Anthropic Setings ------
ANTHROPIC_MAX_CONTEXT_WINDOW: int = int(os.environ["ANTHROPIC_MAX_CONTEXT_WINDOW"])
ANTHROPIC_MAX_TOKENS: int = int(os.environ["ANTHROPIC_MAX_TOKENS"])
ANTHROPIC_DEFAULT_TEMPERATURE: float = float(os.environ["ANTHROPIC_DEFAULT_TEMPERATURE"])
ANTHROPIC_DEFAULT_TOP_P: float = float(os.environ["ANTHROPIC_DEFAULT_TOP_P"])
# -------------------------------

# ------ OpenAI Common Settings ------
OPENAI_DEFAULT_TEMPERATURE: float = float(os.environ["OPENAI_DEFAULT_TEMPERATURE"])
OPENAI_DEFAULT_TOP_P: float = float(os.environ["OPENAI_DEFAULT_TOP_P"])

# OpenAI gpt model
GPT_MAX_CONTEXT_WINDOW: int = int(os.environ["GPT_MAX_CONTEXT_WINDOW"])
GPT_MAX_TOKENS: int = int(os.environ["GPT_MAX_TOKENS"])
# ------------------------------------
