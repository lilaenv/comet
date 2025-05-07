from dataclasses import dataclass
from enum import Enum

from discord import Colour, Embed, Thread

from src.comet.config.env import MAX_CHARS_PER_MESSAGE


class ResponseStatus(Enum):
    """Enumeratino of possible response statuses from text generation service.

    Attributes
    ----------
    SUCCESS : int
        Indicates the response was generated successfully.
    ERROR : int
        Indicates an error occurred during the generation process.
    MODERATION_FLAGGED : int
        Indicates the response was flagged by the moderation system.
    """

    SUCCESS = 0
    ERROR = 1
    MODERATION_FLAGGED = 2


@dataclass
class ResponseResult:
    """Represents the result of a response from the text generation service.

    Attributes
    ----------
    status : ResponseStatus
        The status of the response.
    content : str | None
        The content of the response, or None if generation failed.
    """

    status: ResponseStatus
    content: str | None


def _split_into_shorter_messages(message: str) -> list[str]:
    """Split a long message into multiple shorter messages.

    Parameters
    ----------
    message : str
        The long message needs to be split.

    Returns
    -------
    list[str]
        A list of shorter messages.
    """
    return [
        message[msg : msg + MAX_CHARS_PER_MESSAGE]
        for msg in range(0, len(message), MAX_CHARS_PER_MESSAGE)
    ]


async def send_response_to_thread(thread: Thread, result: ResponseResult) -> None:
    """Send the generated response to the discord thread.

    Parameters
    ----------
    thread : Thread
        The Discord thread where the response will be sent.
    result : ResponseResult
        The result of the response, containing status and content.
    """
    status = result.status
    if status == ResponseStatus.SUCCESS:
        if not result.content:
            msg = "No response generated."
            raise ValueError(msg)
        shorter_response = _split_into_shorter_messages(result.content)
        for res in shorter_response:
            await thread.send(res)
    elif status == ResponseStatus.ERROR:
        await thread.send(
            embed=Embed(
                description="**An error occurred during text generation**",
                color=Colour.red(),
            ),
        )
