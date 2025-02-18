from __future__ import annotations

from discord import Message as DiscordMessage
from discord import Thread

from src.comet._env import (
    ANTHROPIC_MAX_CONTEXT_WINDOW,
    GPT_MAX_CONTEXT_WINDOW,
)
from src.comet.cli import parse_args_and_setup_logging
from src.comet.client.discord_client import DiscordClient

from .claude_command import *
from .gpt_command import *

logger = parse_args_and_setup_logging()
discord_client = DiscordClient.get_instance()


def _is_valid_message(discord_message: DiscordMessage) -> bool:
    return not (
        # ignore messages from the bot
        # blocked user can't use the bot
        # ignore messages not in a thread
        # ignore threads not created by the bot
        # ignore threads that are archived, locked or title is not what we expected
        # ignore threads that have too many messages
        discord_message.author == discord_client.user
        or not isinstance(discord_message.channel, Thread)
        or discord_message.channel.owner_id != discord_client.user.id
        or discord_message.channel.archived
        or discord_message.channel.locked
    )


async def _close_thread(thread: Thread) -> None:
    await thread.send(
        embed=Embed(
            description="closing...",
            color=Colour.light_grey(),
        )
    )
    await thread.edit(archived=False, locked=True)


async def _get_conversation_history(thread: Thread, limit: int) -> list:
    convo_history = [
        await ChatMessage.from_discord_message(message)
        async for message in thread.history(limit=limit)
    ]
    convo_history = [msg for msg in convo_history if msg is not None]
    convo_history.reverse()
    return convo_history


async def _handle_gpt_thread(discord_message: DiscordMessage) -> None:
    if not isinstance(discord_message.channel, Thread):
        return
    if discord_message.channel.message_count > GPT_MAX_CONTEXT_WINDOW:
        await _close_thread(discord_message.channel)
        return

    # Moderate content
    moderation_result = get_moderation_result(discord_message.content)
    if moderation_result.flagged:
        await discord_message.channel.send(
            embed=Embed(
                description="**Your prompt was flagged by moderation system**",
                color=Colour.red(),
            )
        )
        return

    convo_history = await _get_conversation_history(
        discord_message.channel, GPT_MAX_CONTEXT_WINDOW
    )

    async with discord_message.channel.typing():
        response = await generate_completion_result(  # type: ignore
            prompt=convo_history,
            model_tuner=model_data.get_model_config(discord_message.channel.id),
        )
    await send_completion_result(thread=discord_message.channel, result=response)  # type: ignore


async def _handle_claude_thread(discord_message: DiscordMessage) -> None:
    if not isinstance(discord_message.channel, Thread):
        return
    if discord_message.channel.message_count > ANTHROPIC_MAX_CONTEXT_WINDOW:
        await _close_thread(discord_message.channel)
        return

    convo_history = await _get_conversation_history(
        discord_message.channel, ANTHROPIC_MAX_CONTEXT_WINDOW
    )

    async with discord_message.channel.typing():
        response = await generate_anthropic_response(  # type: ignore
            sys_prompt=sys_prompts.get(discord_message.channel.id),
            prompt=convo_history,
            model_tuner=model_data.get_model_config(discord_message.channel.id),
        )
    await send_anthropic_result(thread=discord_message.channel, result=response)  # type: ignore


@discord_client.event
# イベントハンドラ
# 関数名変えると動かない
async def on_message(discord_message: DiscordMessage) -> None:
    """メッセージが送信された時に呼び出される."""
    try:
        if not _is_valid_message(discord_message):
            return

        # channel の型 Thread を明示するため
        if not isinstance(discord_message.channel, Thread):
            return

        channel: Thread = discord_message.channel

        # handle thread based on prefix
        if channel.name.startswith(GPT_THREAD_PREFIX):
            await _handle_gpt_thread(discord_message)
        elif channel.name.startswith(CLAUDE_THREAD_PREFIX):
            await _handle_claude_thread(discord_message)

    except KeyError:
        logger.exception("Current model_data state %s", model_data)
        await channel.send(
            embed=Embed(
                description="Configuration error occurred. Please try again.",
                color=Colour.red(),
            )
        )
    except Exception:
        logger.exception("An error occurred in the on_message event")
        await channel.send(
            embed=Embed(
                description="An error occurred. Please try again later.",
                color=Colour.red(),
            )
        )
