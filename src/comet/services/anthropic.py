from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from anthropic import (
    Anthropic,
)
from discord import Colour, Embed, Thread
from pydantic import BaseModel

from src.comet.cli import parse_args_and_setup_logging

from .chat_manager import ChatHistory, ChatMessage, split_into_shorter_messages

if TYPE_CHECKING:
    from src.comet.config.anthropic_model import AnthropicModelConfig

logger = parse_args_and_setup_logging()

anthropic_client = Anthropic()


class AnthropicStatus(Enum):
    SUCCESS = 0
    ANTHROPIC_ERROR = 1
    UNKNOWN_ERROR = 2


class AnthropicResult(BaseModel):
    status: AnthropicStatus
    anthropic_result: str | None


async def generate_anthropic_response(
    sys_prompt: str, prompt: list[ChatMessage], model_tuner: AnthropicModelConfig
) -> AnthropicResult:
    """Generate a response from the Anthropic model.

    Parameters
    ----------
    sys_prompt : str
        The system instruction.

    prompt : list of ChatMessage
        A list of chat messages forming the conversation history.

    model_tuner : ChatConfig
        Configuration settings for the model, including parameters like
        max_tokens, temperature and top-p sampling.

    Returns
    -------
    AnthropicResult
        An object containing the status of the response, and the
        generated message.

    """
    try:
        convo = ChatHistory(messages=[*prompt, ChatMessage(role="assistant")]).render_message()
        result = anthropic_client.messages.create(
            messages=convo,  # type: ignore
            model=model_tuner.model,
            max_tokens=model_tuner.max_tokens,
            system=sys_prompt,
            temperature=model_tuner.temperature,
            top_p=model_tuner.top_p,
        )
        anthropic_result = result.content[0].text  # type: ignore
        return AnthropicResult(status=AnthropicStatus.SUCCESS, anthropic_result=anthropic_result)
    except Exception as err:
        msg = f"Unexpected error has occurred: {err!s}"
        logger.exception(msg)
        return AnthropicResult(status=AnthropicStatus.UNKNOWN_ERROR, anthropic_result=None)


async def send_anthropic_result(thread: Thread, result: AnthropicResult) -> None:
    """Send the Anthropic status to a Discord thread.

    Parameters
    ----------
    thread : Thread
        The Discord thread where the Anthropic status and message will
        be sent.
    result : AnthropicResult
        The result of the Anthropic process, containing status,
        generated message, and status information.

    """
    status = result.status
    if status == AnthropicStatus.SUCCESS:
        if not result.anthropic_result:
            await thread.send(
                embed=Embed(
                    description="**The assistant's response is empty.**",
                    color=Colour.yellow(),
                )
            )
        else:
            shorter_response = split_into_shorter_messages(result.anthropic_result)
            for res in shorter_response:
                await thread.send(res)
    elif status == AnthropicStatus.UNKNOWN_ERROR:
        await thread.send(
            embed=Embed(
                description="**An unknown error has occurred.**",
                color=Colour.red(),
            )
        )
