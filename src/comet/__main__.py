import os
import signal
from collections.abc import Generator
from contextlib import contextmanager

from dotenv import load_dotenv

from .cli import parse_args_and_setup_logging
from .client.discord_client import DiscordClient
from .commands import *
from .data.sqlite.access_control_dao import AccessControlDAO
from .data.sqlite.moderation_dao import ModerationDAO


@contextmanager
def ignore_signals(signals: list[signal.Signals]) -> Generator[None, None, None]:
    """Temporarily ignore specified signals.

    Parameters
    ----------
    signals : list[signal.Signals]
        A list of signals to ignore.

    Examples
    --------
    >>> with ignore_signals([signal.SIGTERM, signal.SIGINT]):
    ...     # processes whose signals are ignored
    ...     pass

    """
    original_handlers = {sig: signal.getsignal(sig) for sig in signals}
    try:
        for sig in signals:
            signal.signal(sig, signal.SIG_IGN)
        yield
    finally:
        for sig, handler in original_handlers.items():
            signal.signal(sig, handler)


async def main() -> None:  # noqa: D103
    logger = parse_args_and_setup_logging()

    await AccessControlDAO().create_table()
    await ModerationDAO().create_table()

    load_dotenv()
    # ここでしか使わない環境変数だよー
    # This environment variable is specific to this function
    DISCORD_BOT_TOKEN: str = os.environ["DISCORD_BOT_TOKEN"]  # noqa: N806

    discord_client = DiscordClient.get_instance()

    try:
        await discord_client.start(DISCORD_BOT_TOKEN)
    except Exception:
        logger.exception("An unexpected error occurred")
    finally:
        with ignore_signals([signal.SIGTERM, signal.SIGINT]):
            await discord_client.cleanup_hook()
            logger.info("Cleanup process finished")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
