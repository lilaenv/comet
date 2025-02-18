from __future__ import annotations

from collections import defaultdict
from typing import Literal

from discord import (
    Colour,
    Embed,
    HTTPException,
    Interaction,
    app_commands,
)

from src.comet._env import (
    GPT_MAX_TOKENS,
    OPENAI_DEFAULT_TEMPERATURE,
    OPENAI_DEFAULT_TOP_P,
)
from src.comet.cli import parse_args_and_setup_logging
from src.comet.client.discord_client import DiscordClient
from src.comet.config.openai_model import OpenAIModelConfig
from src.comet.data.sqlite.access_control_dao import AccessControlDAO
from src.comet.services.chat_manager import ChatMessage
from src.comet.services.completion import *
from src.comet.services.moderation import get_moderation_result
from src.comet.utils.access_control import *

logger = parse_args_and_setup_logging()

access_control_dao = AccessControlDAO()
discord_client = DiscordClient.get_instance()

GPT_THREAD_PREFIX: Literal["g:"] = "g:"
ADVANCED_USER_IDS: list[int] = access_control_dao.fetch_user_ids_by_access_type(
    access_type="advanced",
)
BLOCKED_USER_IDS: list[int] = access_control_dao.fetch_user_ids_by_access_type(
    access_type="blocked",
)

model_data: defaultdict = defaultdict()


@discord_client.tree.command(
    name="gpt", description="スレッドを作成し、AIとのチャットを開始します"
)
@app_commands.choices(
    model=[
        app_commands.Choice(name="gpt-4o-mini", value=100),
        app_commands.Choice(name="gpt-4o", value=101),
    ]
)
@is_authorized_server()  # type: ignore
@is_not_blocked_user()  # type: ignore
async def gpt_command(
    interaction: Interaction,
    prompt: str,
    model: app_commands.Choice[int],
    temperature: float = OPENAI_DEFAULT_TEMPERATURE,
    top_p: float = OPENAI_DEFAULT_TOP_P,
) -> None:
    """Create a new thread and start a chat with the assistant."""
    try:
        user = interaction.user
        logger.info("%s executed gpt command: %s", user, prompt[:20])

        if temperature < 0.0 or temperature > 2.0:  # noqa: PLR2004
            await interaction.response.send_message(
                "**temperature**は 0.0 から２.0 の間で設定してください",
                ephemeral=True,
            )
            return
        if top_p < 0.0 or top_p > 1.0:
            await interaction.response.send_message(
                "**top_p**は 0.0 から１.0 の間で設定してください",
                ephemeral=True,
            )
            return

        # ------ moderate user's prompt ------
        moderation_result = get_moderation_result(prompt)
        if moderation_result.flagged:
            await interaction.response.send_message(
                embed=Embed(
                    description="**Your prompt was flagged by moderation system**",
                    color=Colour.red(),
                )
            )
            return
        # ------------------------------------

        # ------ define embed style ------
        embed = Embed(
            description=f"<@{user.id}> initiated the chat!",
            color=Colour.gold(),
        )
        embed.add_field(name="model", value=model.name, inline=True)
        embed.add_field(name="temperature", value=temperature, inline=True)
        embed.add_field(name="top_p", value=top_p, inline=True)
        embed.add_field(name="message", value=prompt)
        # --------------------------------

        await interaction.response.send_message(embed=embed)
        original_response = await interaction.original_response()

        # create the thread
        thread = await original_response.create_thread(
            name=f"{GPT_THREAD_PREFIX} {prompt[:30]}",
            auto_archive_duration=60,
            slowmode_delay=1,
        )
        model_data[thread.id] = OpenAIModelConfig(
            model=model.name,
            max_tokens=GPT_MAX_TOKENS,
            temperature=temperature,
            top_p=top_p,
        )
        async with thread.typing():
            messages = [ChatMessage(role=user.name, content=prompt)]
            response = await generate_completion_result(  # type: ignore
                prompt=messages,
                model_tuner=model_data[thread.id],
            )
        await send_completion_result(  # type: ignore
            thread=thread,
            result=response,
        )
    except HTTPException:
        await interaction.response.send_message(
            "**HTTPException**: 管理者に報告してください",
        )
        logger.exception("HTTPException occurred in the chat command")
    except Exception:
        logger.exception("An error occurred in the chat command")


@discord_client.tree.error
async def on_app_command_error(  # noqa: D103
    interaction: Interaction, error: app_commands.AppCommandError
) -> None:
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message(
            "**CheckFailure:** このコマンドを実行する権限がありません。", ephemeral=True
        )
