import aiosqlite

from src.comet.sqlite.sqlite_db_base import SQLiteDbBase


class ModerationDAO(SQLiteDbBase):
    _table_name = "moderation"

    async def create_table(self) -> None:
        if not self.validate_table_name(self._table_name):
            msg = "Invalid table name: Only alphanumeric characters and underscores are allowed."
            raise ValueError(msg)

        conn = await aiosqlite.connect(super().DB_NAME)
        try:
            query = f"""
            CREATE TABLE IF NOT EXISTS {self._table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                moderation_id TEXT NOT NULL,
                category_scores TEXT NOT NULL,
                flagged BOOLEAN NOT NULL,
            );
            """
            await conn.execute(query)
            await conn.commit()
        finally:
            await conn.close()
