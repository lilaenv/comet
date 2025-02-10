import os
import re

from dotenv import load_dotenv

load_dotenv()


class SQLiteDbBase:
    """Base class for SQLite database."""

    # 環境変数は通常 _env.py でロードする
    # sqlite に関するロジックはこのディレクトリに集約する
    # そのためここで SQLITE_DB_NAME をロードする
    DB_NAME: str = os.environ["SQLITE_DB_NAME"]

    @staticmethod
    def validate_table_name(table_name: str) -> bool:
        """Only letters, numbers, and underscores are allowed."""
        pattern = r"^[A-Za-z0-9_]+$"
        return bool(re.match(pattern, table_name))
