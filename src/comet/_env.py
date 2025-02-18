import os

from discord import app_commands
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


# 利用可能なモデルを取得
def get_model_choices(env_var: str) -> list[app_commands.Choice[int]]:
    models_str = os.environ[env_var]
    choices: list[app_commands.Choice[int]] = []
    if models_str:
        for entry in models_str.split(","):
            entry_stripped = entry.strip()
            if not entry_stripped:
                msg = "Empty"
                raise ValueError(msg)
            try:
                name, value_str = entry_stripped.split(":")
                value = int(value_str)
            except ValueError as err:
                msg = "Invalid format"
                raise ValueError(msg) from err
            choices.append(app_commands.Choice(name=name, value=value))
    return choices


claude_choices = get_model_choices("ANTHROPIC_MODELS")
gpt_choices = get_model_choices("GPT_MODELS")
