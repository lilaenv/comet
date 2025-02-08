from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytz
from dotenv import load_dotenv

if TYPE_CHECKING:
    from pytz import _UTCclass
    from pytz.tzinfo import DstTzInfo, StaticTzInfo

# 環境変数は通常 _env.py でロードする
# TIMEZONE は 最終的にタイムゾーンオブジェクトとなる
# この流れを明確にするため、TIMEZONE はここでロードする
load_dotenv()
_tz: str = os.environ["TIMEZONE"]
TIMEZONE: _UTCclass | DstTzInfo | StaticTzInfo = pytz.timezone(_tz)
