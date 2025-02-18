from __future__ import annotations

from typing import Literal

from discord import (
    Colour,
    Embed,
    HTTPException,
    Interaction,
    app_commands,
)

from src.comet._env import (
    ANTHROPIC_DEFAULT_TEMPERATURE,
    ANTHROPIC_DEFAULT_TOP_P,
    ANTHROPIC_MAX_TOKENS,
)
from src.comet._yml import CLAUDE_SYSTEM
from src.comet.cli import parse_args_and_setup_logging
from src.comet.client.discord_client import DiscordClient
from src.comet.config.anthropic_model import AnthropicModelConfig
from src.comet.data.sqlite.access_control_dao import AccessControlDAO
from src.comet.services.anthropic import *
from src.comet.services.chat_manager import ChatMessage
from src.comet.utils.access_control import *

logger = parse_args_and_setup_logging()

access_control_dao = AccessControlDAO()
discord_client = DiscordClient.get_instance()

CLAUDE_THREAD_PREFIX: Literal["c:"] = "c:"
ADVANCED_USER_IDS: list[int] = access_control_dao.fetch_user_ids_by_access_type(
    access_type="advanced",
)
BLOCKED_USER_IDS: list[int] = access_control_dao.fetch_user_ids_by_access_type(
    access_type="blocked",
)

model_data: dict = {}


@discord_client.tree.command(
    name="claude", description="スレッドを作成し、AIとのチャットを開始します"
)
@app_commands.choices(
    model=[
        app_commands.Choice(name="claude-3-5-haiku-20241022", value=500),
        app_commands.Choice(name="claude-3-5-sonnet-20241022", value=501),
    ]
)
@is_authorized_server()  # type: ignore
@is_advanced_user()  # type: ignore
@is_not_blocked_user()  # type: ignore
async def claude_command(  # noqa: PLR0913
    interaction: Interaction,
    prompt: str,
    model: app_commands.Choice[int],
    sys_prompt: str = CLAUDE_SYSTEM,
    temperature: float = ANTHROPIC_DEFAULT_TEMPERATURE,
    top_p: float = ANTHROPIC_DEFAULT_TOP_P,
) -> None:
    """Create a new thread and start a chat with the assistant."""
    try:
        user = interaction.user
        logger.info("%s executed claude command: %s", user, prompt[:20])

        if temperature < 0.0 or temperature > 1.0:
            await interaction.response.send_message(
                "**temperature**は 0.0 から1.0 の間で設定してください",
                ephemeral=True,
            )
            return
        if top_p < 0.0 or top_p > 1.0:
            await interaction.response.send_message(
                "**top_p**は 0.0 から１.0 の間で設定してください",
                ephemeral=True,
            )
            return

        # ------ define embed style ------
        embed = Embed(
            description=f"<@{user.id}> initiated the chat!",
            color=Colour.orange(),
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
            name=f"{CLAUDE_THREAD_PREFIX} {prompt[:30]}",
            auto_archive_duration=60,
            slowmode_delay=1,
        )
        model_data[thread.id] = AnthropicModelConfig(
            model=model.name,
            max_tokens=ANTHROPIC_MAX_TOKENS,
            temperature=temperature,
            top_p=top_p,
        )
        async with thread.typing():
            messages = [ChatMessage(role=user.name, content=prompt)]
            response = await generate_anthropic_response(  # type: ignore
                sys_prompt=sys_prompt,
                prompt=messages,
                model_tuner=model_data[thread.id],
            )
        await send_anthropic_result(  # type: ignore
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
