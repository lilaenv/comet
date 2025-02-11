import aiosqlite

from src.comet.data.dto.moderation_dto import ModerationDTO

from .sqlite_db_base import SQLiteDbBase


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
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                moderation_id   TEXT NOT NULL,
                category_scores TEXT NOT NULL,
                flagged         BOOLEAN NOT NULL
            );
            """
            await conn.execute(query)
            await conn.commit()
        finally:
            await conn.close()

    async def insert(self, moderation_result: ModerationDTO) -> None:
        # フラグが True のときのみ記録する
        if moderation_result.flagged is False:
            return
        conn = await aiosqlite.connect(super().DB_NAME)
        try:
            query = """
            INSERT INTO moderation (moderation_id, category_scores, flagged)
            VALUES (?, ?, ?);
            """
            await conn.execute(
                query,
                (
                    moderation_result.moderation_id,
                    moderation_result.category_scores,
                    moderation_result.flagged,
                ),
            )
            await conn.commit()
        finally:
            await conn.close()
