from __future__ import annotations

from discord import Message as DiscordMessage
from discord import MessageType
from pydantic import BaseModel

from src.comet._env import MAX_CHARS_PER_RESPONSE


class ChatMessage(BaseModel):
    """Represents a single chat message with a role and content.

    Attributes
    ----------
    role : str
        The role of the message sender, e.g., 'developer', 'assistant',
        or 'user'.
    content : str or None, optional
        The content of the message. Defaults to None.

    """

    role: str
    content: str | None = None

    def format_message(self) -> dict[str, str]:
        """Represent a single chat message with a role and content.

        Returns
        -------
        dict
            A dictionary with 'role' and 'content' keys.

        """
        return {
            "role": self.role if self.role in ("developer", "assistant") else "user",
            "content": self.content or "",
        }

    @classmethod
    def from_discord_message(cls, message: DiscordMessage) -> ChatMessage | None:
        """Convert a DiscordMessage instance to a ChatMessage instance.

        Parameters
        ----------
        message : DiscordMessage
            A message from Discord, which may be a thread starter or a
            regular message.

        Returns
        -------
        ChatMessage or None
            A ChatMessage instance if the conversion is successful,
            otherwise None.

        Examples
        --------
        >>> discord_msg = ...  # Discord message object
        >>> chat_msg = ChatMessage.from_discord_message(discord_msg)
        >>> if chat_msg:
        ...     print(chat_msg.format_message())

        """
        # スレッド作成時の処理
        if (
            message.type == MessageType.thread_starter_message
            and message.reference is not None
            and message.reference.cached_message
            and message.reference.cached_message.embeds
            and message.reference.cached_message.embeds[0].fields
        ):
            field = message.reference.cached_message.embeds[0].fields[0]
            return cls(role=message.author.name, content=field.value)
        # 通常のメッセージ処理
        if message.content:
            return cls(role=message.author.name, content=message.content)
        return None


class ChatHistory(BaseModel):
    """Manage a collection of chat messages.

    Attributes
    ----------
    messages : list of ChatMessage
        A list of ChatMessage objects representing the chat history.

    """

    messages: list[ChatMessage]

    def render_message(self) -> list[dict[str, str]]:
        """Render the chat messages into a list of dictionaries.

        Returns
        -------
        list of dict
            A list where each dictionary represents a chat message with
            'role' and 'content' keys.

        """
        return [message.format_message() for message in self.messages]


def split_into_shorter_messages(message: str) -> list[str]:
    """Split a long message into multiple shorter messages.

    Parameters
    ----------
    message : str
        The long message string that needs to be split.

    Returns
    -------
    list of str
        A list of message segments, each within the character limit.

    """
    return [
        message[i : i + MAX_CHARS_PER_RESPONSE]
        for i in range(0, len(message), MAX_CHARS_PER_RESPONSE)
    ]
