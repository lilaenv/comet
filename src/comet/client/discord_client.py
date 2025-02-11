from discord import Client, Intents, app_commands

from src.comet.cli import parse_args_and_setup_logging

logger = parse_args_and_setup_logging()

intents = Intents.default()
intents.message_content = True
intents.members = True


class DiscordClient(Client):
    _instance: "DiscordClient"
    tree: app_commands.CommandTree

    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    @classmethod
    def get_instance(cls) -> "DiscordClient":
        """Get the singleton instance of the DiscordClient class.

        Returns
        -------
        DiscordClient
            The instance of the DiscordClient class.

        """
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    async def setup_hook(self) -> None:
        synced_cmds = await self.tree.sync()
        logger.info("Setup hook completed")
        logger.info("Synced %d commands", len(synced_cmds))

    async def on_ready(self) -> None:
        logger.info("%s is ready", self.user)
        for cmd in self.tree.walk_commands():
            logger.info("Command Name: %s", cmd.name)

    async def cleanup_hook(self) -> None:
        logger.info("Start cleanup ...")
