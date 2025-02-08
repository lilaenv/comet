from __future__ import annotations

import logging
from pathlib import Path


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

    logging.basicConfig(
        level=log_level,
        # [2025-01-27 00:13:26 - <filename>:102 - DEBUG] <message>
        format="[%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),  # output logs to a .log
            logging.StreamHandler(),  # output logs to console
        ],
    )

    return logging.getLogger(__name__)
