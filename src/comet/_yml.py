from pathlib import Path

import yaml

# system.yml ファイルを読み込む
with Path(__file__).parent.parent.parent.joinpath(".prompt.yml").open(encoding="utf-8") as f:
    config = yaml.safe_load(f)

# system_prompt キーを取得
CLAUDE_SYSTEM_PROMPT: str = config.get("claude_system_prompt")
GPT_SYSTEM_PROMPT: str = config.get("gpt_system_prompt")
