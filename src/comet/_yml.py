from pathlib import Path

import yaml

# system.yml ファイルを読み込む
with Path(__file__).parent.parent.parent.joinpath(".prompt.yml").open(encoding="utf-8") as f:
    config = yaml.safe_load(f)

# system_prompt キーを取得
SYSTEM_PROMPT: str = config.get("system_prompt")
