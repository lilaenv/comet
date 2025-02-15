from __future__ import annotations

from collections import defaultdict
from typing import Literal

from discord import (
    Colour,
    Embed,
    HTTPException,
    Interaction,
    Thread,
    app_commands,
)
from discord import Message as DiscordMessage

from src.comet._env import MAX_CONTEXT_WINDOW, TEMPERATURE, TOP_P
from src.comet.cli import parse_args_and_setup_logging
from src.comet.client.discord_client import DiscordClient
from src.comet.config.openai_model import ModelConfig
from src.comet.data.sqlite.access_control_dao import AccessControlDAO
from src.comet.services.chat_manager import ChatMessage
from src.comet.services.completion import *
from src.comet.services.moderation import get_moderation_result
from src.comet.utils.access_control import *

logger = parse_args_and_setup_logging()

access_control_dao = AccessControlDAO()
discord_client = DiscordClient.get_instance()

ACTIVATE_THREAD_PREFIX: Literal[">>>"] = ">>>"
ADVANCED_USER_IDS: list[int] = access_control_dao.fetch_user_ids_by_access_type(
    access_type="advanced",
)
BLOCKED_USER_IDS: list[int] = access_control_dao.fetch_user_ids_by_access_type(
    access_type="blocked",
)

model_data = defaultdict()


@discord_client.tree.command(
    name="chat", description="スレッドを作成し、AIとのチャットを開始します"
)
@app_commands.choices(
    model=[
        app_commands.Choice(name="gpt-4o-mini", value=100),
        app_commands.Choice(name="gpt-4o", value=101),
    ]
)
@is_authorized_server()
@is_not_blocked_user()
async def chat_command(
    interaction: Interaction,
    prompt: str,
    model: app_commands.Choice[int],
    temperature: float | None = TEMPERATURE,
    top_p: float | None = TOP_P,
) -> None:
    """Create a new thread and start a chat with the assistant."""
    try:
        user = interaction.user
        logger.info("%s executed chat command: %s", user, prompt[:20])

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
            name=f"{ACTIVATE_THREAD_PREFIX} {prompt[:30]}",
            auto_archive_duration=60,
            slowmode_delay=1,
        )
        model_data[thread.id] = ModelConfig(
            model=model.name,
            temperature=temperature,
            top_p=top_p,
        )
        async with thread.typing():
            messages = [ChatMessage(role=user.name, content=prompt)]
            response = await generate_completion_result(
                prompt=messages,
                model_tuner=model_data[thread.id],
            )
        await send_completion_result(
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


@discord_client.event
# イベントハンドラ
# 関数名変えると動かない
@is_authorized_server()
async def on_message(discord_message: DiscordMessage) -> None:  # noqa: D103
    try:
        # ignore messages from the bot
        # blocked user can't use the bot
        # ignore messages not in a thread
        # ignore threads not created by the bot
        # ignore threads that are archived, locked or title is not what we expected
        # ignore threads that have too many messages
        if (
            discord_message.author == discord_client.user
            or not isinstance(discord_message.channel, Thread)
            or discord_message.channel.owner_id != discord_client.user.id
            or discord_message.channel.archived
            or discord_message.channel.locked
            or not discord_message.channel.name.startswith(ACTIVATE_THREAD_PREFIX)
        ):
            await thread.send(
                embed=Embed(
                    description="無効なスレッドです",
                    color=Colour.dark_grey(),
                ),
            )
            return

        channel = discord_message.channel
        thread = channel

        # check if the thread has too many messages
        if thread.message_count > MAX_CONTEXT_WINDOW:
            await thread.send(
                embed=Embed(
                    description="Context limit reached, closing...",
                    color=Colour.light_grey(),
                )
            )
            await thread.edit(archived=False, locked=True)
            return

        # ------ moderate user's message ------
        moderation_result = get_moderation_result(discord_message.content)
        if moderation_result.flagged:
            await discord_message.channel.send(
                embed=Embed(
                    description="**Your prompt was flagged by moderation system**",
                    color=Colour.red(),
                )
            )
            return

        # ------ get conversation history ------
        convo_history = [
            await ChatMessage.from_discord_message(message)
            async for message in thread.history(limit=MAX_CONTEXT_WINDOW)
        ]
        convo_history = [msg for msg in convo_history if msg is not None]
        convo_history.reverse()

        # ------ generate the response ------
        async with thread.typing():
            response = await generate_completion_result(
                prompt=convo_history,
                model_tuner=model_data[thread.id],
            )
        await send_completion_result(thread=thread, result=response)
    except Exception:
        logger.exception("An error occurred in the on_message event")


@discord_client.tree.error
async def on_app_command_error(  # noqa: D103
    interaction: Interaction, error: app_commands.AppCommandError
) -> None:
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message(
            "**CheckFailure:** このコマンドを実行する権限がありません。", ephemeral=True
        )
