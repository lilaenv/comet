import datetime

import aiosqlite

from src.comet.config.timezone import TIMEZONE
from src.comet.data.dto.user_dto import UserDTO

from .sqlite_db_base import SQLiteDbBase


class AccessControlDAO(SQLiteDbBase):
    _table_name = "access_control"

    async def create_table(self) -> None:
        if not self.validate_table_name(self._table_name):
            msg = "Invalid table name: Only alphanumeric characters and underscores are allowed."
            raise ValueError(msg)

        conn = await aiosqlite.connect(super().DB_NAME)
        try:
            query = f"""
            CREATE TABLE IF NOT EXISTS {self._table_name} (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                access_type TEXT NOT NULL,
                add_date    DATE NOT NULL,
                rm_date     DATE DEFAULT NULL
            );
            """
            await conn.execute(query)
            await conn.commit()
        finally:
            await conn.close()

    async def insert(self, user_id: UserDTO, access_type: str) -> None:
        conn = await aiosqlite.connect(super().DB_NAME)
        date = datetime.datetime.now(TIMEZONE).date()
        try:
            query = """
            INSERT INTO access_control (user_id, access_type, add_date)
            VALUES (?, ?, ?);
            """
            await conn.execute(query, (user_id.user_id, access_type, date))
            await conn.commit()
        finally:
            await conn.close()

    async def fetch_user_ids_by_access_type(self, access_type: str) -> list[int]:
        conn = await aiosqlite.connect(super().DB_NAME)
        try:
            query = """
            SELECT user_id FROM access_control WHERE access_type = ? AND rm_date IS NULL;
            """
            cursor = await conn.execute(query, (access_type,))
            rows = await cursor.fetchall()
            return [row[0] for row in rows]
        finally:
            await conn.close()

    async def remove(self, user_id: UserDTO, access_type: str) -> None:
        conn = await aiosqlite.connect(super().DB_NAME)
        date = datetime.datetime.now(TIMEZONE).date()
        try:
            query = """
            UPDATE access_control SET rm_date = ? WHERE user_id = ? AND access_type = ?;
            """
            await conn.execute(query, (date, user_id.user_id, access_type))
            await conn.commit()
        finally:
            await conn.close()
