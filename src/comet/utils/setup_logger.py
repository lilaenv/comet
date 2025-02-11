from __future__ import annotations

import logging
from collections.abc import Mapping
from pathlib import Path
from typing import override

from src.comet._env import SYSTEM_PROMPT


class SensitiveSystemPromptFilter(logging.Filter):
    @override
    def filter(self, record: logging.LogRecord) -> bool:
        # record.argsが辞書で、'json_data'キーが存在し、その値も辞書の場合に処理する
        if isinstance(record.args, Mapping) and "json_data" in record.args:
            json_data = record.args["json_data"]
            if isinstance(json_data, Mapping) and "messages" in json_data:
                messages = json_data["messages"]
                # messagesがリストの場合、各メッセージをチェック
                if isinstance(messages, list):
                    for msg in messages:
                        if (
                            isinstance(msg, Mapping)
                            and msg.get("role") == "developer"
                            and msg.get("content") == SYSTEM_PROMPT
                        ):
                            msg["content"] = "<redacted>"
        return True


def setup_logger(log_level: str | int) -> logging.Logger:
    """Set up a logger for the calling file.

    Parameters
    ----------
    log_level : str or int
        The logging level. Can be specified either as a string or
        integer constant.
        Valid string values (case-insensitive):
        - 'DEBUG'
        - 'INFO'
        - 'WARNING'
        - 'ERROR'
        - 'CRITICAL'

        or corresponding integer constants:
        - logging.DEBUG (10)
        - logging.INFO (20)
        - logging.WARNING (30)
        - logging.ERROR (40)
        - logging.CRITICAL (50)

    Returns
    -------
    logging.Logger
        Configured logger instance with the specified log level and
        handlers for both file and console output.

    Raises
    ------
    TypeError
        If the provided log level is not a valid string values or
        integer constants.

    """
    # log_level が文字列なら大文字に変換して、対応する logging 定数を取得
    if isinstance(log_level, str):
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            msg = f"Invalid log level: {log_level}"
            raise TypeError(msg)
        log_level = numeric_level

    log_file = "./logs/comet.log"

    # logs フォルダが存在しなければ作成
    Path("./logs").mkdir(exist_ok=True)

    # ハンドラを個別に作成
    file_handler = logging.FileHandler(log_file)
    stream_handler = logging.StreamHandler()

    # SensitiveSystemPromptFilter を各ハンドラに追加
    sensitive_filter = SensitiveSystemPromptFilter()
    file_handler.addFilter(sensitive_filter)
    stream_handler.addFilter(sensitive_filter)

    logging.basicConfig(
        level=log_level,
        # [2025-01-27 00:13:26 - <filename>:102 - DEBUG] <message>
        format="[%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s] %(message)s",
        handlers=[
            file_handler,  # output logs to a .log
            stream_handler,  # output logs to console
        ],
    )

    return logging.getLogger(__name__)
