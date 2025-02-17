from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from discord import Colour, Embed, Thread
from openai import (
    APIConnectionError,
    APITimeoutError,
    BadRequestError,
    InternalServerError,
    OpenAI,
)
from pydantic import BaseModel

from src.comet._env import (
    MAX_TOKENS,
    SEPARATOR_TOKEN,
)
from src.comet._yml import SYSTEM_PROMPT
from src.comet.cli import parse_args_and_setup_logging
from src.comet.data.sqlite.moderation_dao import ModerationDAO

from .chat_manager import ChatHistory, ChatMessage, split_into_shorter_messages
from .moderation import get_moderation_result

if TYPE_CHECKING:
    from src.comet.config.openai_model import ModelConfig

logger = parse_args_and_setup_logging()

moderation_dao = ModerationDAO()
openai_client = OpenAI()


class CompletionStatus(Enum):
    SUCCESS = 0
    OPENAI_ERROR = 1
    UNKNOWN_ERROR = 2
    MODERATION_FLAGGED = 3


class CompletionResult(BaseModel):
    status: CompletionStatus
    completion_result: str | None


async def generate_completion_result(
    prompt: list[ChatMessage], model_tuner: ModelConfig
) -> CompletionResult:
    """Generate a response from the OpenAI model.

    Parameters
    ----------
    prompt : list of ChatMessage
        A list of chat messages forming the conversation history.
    user : Member or User
        The Discord user or member initiating the request.
    model_tuner : ChatConfig
        Configuration settings for the model, including parameters like
        temperature and top-p sampling.

    Returns
    -------
    CompletionResult
        An object containing the status of the completion, the
        generated message, and any additional status information.

    """
    try:
        convo = ChatHistory(messages=[*prompt, ChatMessage(role="assistant")]).render_message()
        full_prompt = [{"role": "developer", "content": SYSTEM_PROMPT}, *convo]
        completion = openai_client.chat.completions.create(
            messages=full_prompt,
            model=model_tuner.model,
            max_tokens=MAX_TOKENS,
            temperature=model_tuner.temperature,
            top_p=model_tuner.top_p,
            stop=SEPARATOR_TOKEN,
        )
        completion_result = completion.choices[0].message.content

        # ------ moderate the assistant's responses ------
        moderation_result = get_moderation_result(completion_result)
        await moderation_dao.insert(moderation_result)
        return CompletionResult(
            status=CompletionStatus.SUCCESS, completion_result=completion_result
        )
    except (APIConnectionError, APITimeoutError, BadRequestError) as err:
        msg = f"Failed to generate completion: {err!s}"
        logger.exception(msg)
        return CompletionResult(status=CompletionStatus.OPENAI_ERROR, completion_result=None)
    except InternalServerError as err:
        msg = f"InternalServerError has occurred: {err!s}"
        logger.exception(msg)
        return CompletionResult(status=CompletionStatus.OPENAI_ERROR, completion_result=None)
    except Exception as err:
        msg = f"Unexpected error has occurred: {err!s}"
        logger.exception(msg)
        return CompletionResult(status=CompletionStatus.UNKNOWN_ERROR, completion_result=None)


async def send_completion_result(thread: Thread, result: CompletionResult) -> None:
    """Send the completion status to a Discord thread.

    Parameters
    ----------
    thread : Thread
        The Discord thread where the completion status and message will
        be sent.
    result : CompletionResult
        The result of the completion process, containing status,
        generated message, and status information.

    """
    status = result.status
    if status == CompletionStatus.SUCCESS:
        if not result.completion_result:
            await thread.send(
                embed=Embed(
                    description="**The assistant's response is empty.**",
                    color=Colour.yellow(),
                )
            )
        else:
            shorter_response = split_into_shorter_messages(result.completion_result)
            for res in shorter_response:
                await thread.send(res)
    elif status == CompletionStatus.OPENAI_ERROR:
        await thread.send(
            embed=Embed(
                description="**An error has occurred while generating the completion.**",
                color=Colour.red(),
            )
        )
    elif status == CompletionStatus.UNKNOWN_ERROR:
        await thread.send(
            embed=Embed(
                description="**An unknown error has occurred.**",
                color=Colour.red(),
            )
        )
    elif status == CompletionStatus.MODERATION_FLAGGED:
        await thread.send(
            embed=Embed(
                description="**The assistant's response was flagged by moderation system.**",
                color=Colour.red(),
            )
        )
