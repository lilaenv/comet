import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

# Discord Settings
AUTHORIZED_SERVER_IDS: list[int] = list(map(int, os.environ["AUTHORIZED_SERVER_IDS"].split(",")))
ADMIN_USER_IDS: list[int] = list(map(int, os.environ["ADMIN_USER_IDS"].split(",")))
MAX_CHARS_PER_RESPONSE: int = int(os.environ["MAX_CHARS_PER_RESPONSE"])

# OpenAI Settings
AVAILABLE_MODELS: list[str] = os.environ["AVAILABLE_MODELS"].split(",")
DEFAULT_MODEL: str = os.environ["DEFAULT_MODEL"]
MAX_CONTEXT_WINDOW: int = int(os.environ["MAX_CONTEXT_WINDOW"])
MAX_TOKENS: int = int(os.environ["MAX_TOKENS"])
SEPARATOR_TOKEN: str = os.environ["SEPARATOR_TOKEN"]

# system.yml ファイルを読み込む
with Path(__file__).parent.parent.parent.joinpath(".prompt.yml").open(encoding="utf-8") as f:
    config = yaml.safe_load(f)

# YAML 内の system_prompt キーを取得
SYSTEM_PROMPT: str = config.get("system_prompt")
