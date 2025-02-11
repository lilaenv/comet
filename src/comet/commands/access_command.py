from discord import Interaction, SelectOption, User, app_commands
from discord.ui import Select, View

from src.comet.cli import parse_args_and_setup_logging
from src.comet.client.discord_client import DiscordClient
from src.comet.data.sqlite.access_control_dao import AccessControlDAO
from src.comet.utils.access_control import is_admin_user, is_authorized_server

logger = parse_args_and_setup_logging()

discord_client = DiscordClient.get_instance()

access_control_dao = AccessControlDAO()


class AccessAddSelector(Select):
    def __init__(self, user_id: int, options: list[SelectOption]):
        self.user_id = user_id
        super().__init__(
            placeholder="Select a access type ...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: Interaction) -> None:
        chosen = self.values[0]  # "advanced" or "blocked"
        if chosen == "advanced":
            await access_control_dao.insert(user_id=self.user_id, access_type="advanced")
        elif chosen == "blocked":
            await access_control_dao.insert(user_id=self.user_id, access_type="blocked")

        await interaction.response.send_message(
            f"Access type `{chosen}` has been added to the user (ID: `{self.user_id}`)",
            ephemeral=True,
        )
        logger.info("Access type <%s> has been added to the user (ID: %s)", chosen, self.user_id)


class AccessRemoveSelector(Select):
    def __init__(self, user_id: int, options: list[SelectOption]):
        self.user_id = user_id
        super().__init__(
            placeholder="Select a access type ...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: Interaction) -> None:
        chosen = self.values[0]  # "advanced" or "blocked"
        if chosen == "advanced":
            await access_control_dao.delete(user_id=self.user_id, access_type="advanced")
        elif chosen == "blocked":
            await access_control_dao.delete(user_id=self.user_id, access_type="blocked")

        await interaction.response.send_message(
            f"Access type `{chosen}` has been removed from the user (ID: `{self.user_id}`)",
            ephemeral=True,
        )
        logger.info(
            "Access type <%s> has been removed from the user (ID: %s)", chosen, self.user_id
        )


@discord_client.tree.command(name="add_access", description="Add a access type to the user")
@is_authorized_server()
@is_admin_user()
async def add_access_command(interaction: Interaction, user: User) -> None:  # noqa: D103
    target_user_id = user.id
    target_user = interaction.guild.get_member(target_user_id)
    if target_user is None:
        await interaction.response.send_message(
            "The user does not exist in the guild",
            ephemeral=True,
        )
        return

    options = [
        SelectOption(label="advanced", value="advanced"),
        SelectOption(label="blocked", value="blocked"),
    ]

    select = AccessAddSelector(user_id=target_user_id, options=options)
    view = View()
    view.add_item(select)

    await interaction.response.send_message(
        "Select a access type to add to the user",
        view=view,
        ephemeral=True,
    )


@discord_client.tree.command(name="check_access", description="Check the access type of the user")
@is_authorized_server()
@is_admin_user()
async def check_access_command(interaction: Interaction, user: User) -> None:  # noqa: D103
    target_user_id = user.id
    target_user = interaction.guild.get_member(target_user_id)
    if target_user is None:
        await interaction.response.send_message(
            "The user does not exist in the guild",
            ephemeral=True,
        )
        return

    advanced_user_ids = await access_control_dao.fetch_user_ids_by_access_type("advanced")
    blocked_user_ids = await access_control_dao.fetch_user_ids_by_access_type("blocked")

    if advanced_user_ids and blocked_user_ids:
        await interaction.response.send_message(
            f"The user (ID: `{target_user_id}`) has the access type `advanced` and `blocked`",
            ephemeral=True,
        )
        return
    if advanced_user_ids:
        await interaction.response.send_message(
            f"The user (ID: `{target_user_id}`) has the access type `advanced`",
            ephemeral=True,
        )
        return
    if blocked_user_ids:
        await interaction.response.send_message(
            f"The user (ID: `{target_user_id}`) has the access type `blocked`",
            ephemeral=True,
        )
        return
    await interaction.response.send_message(
        f"The user (ID: `{target_user_id}`) does not have any access type",
        ephemeral=True,
    )


@discord_client.tree.command(name="rm_access", description="Remove a access type from the user")
@is_authorized_server()
@is_admin_user()
async def remove_access_command(interaction: Interaction, user: User) -> None:  # noqa: D103
    target_user_id = user.id
    target_user = interaction.guild.get_member(target_user_id)
    if target_user is None:
        await interaction.response.send_message(
            "The user does not exist in the guild",
            ephemeral=True,
        )
        return

    options = [
        SelectOption(label="advanced", value="advanced"),
        SelectOption(label="blocked", value="blocked"),
    ]

    select = AccessRemoveSelector(user_id=target_user_id, options=options)
    view = View()
    view.add_item(select)

    await interaction.response.send_message(
        "Select a access type to remove from the user",
        view=view,
        ephemeral=True,
    )


@discord_client.tree.error
async def on_app_command_error(  # noqa: D103
    interaction: Interaction, error: app_commands.AppCommandError
) -> None:
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message(
            "**CheckFailure:** このコマンドを実行する権限がありません", ephemeral=True
        )
