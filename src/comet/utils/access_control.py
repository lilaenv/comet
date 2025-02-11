from typing import Callable, TypeVar

from discord import Interaction, app_commands

from src.comet._env import ADMIN_USER_IDS, AUTHORIZED_SERVER_IDS
from src.comet.data.sqlite.access_control_dao import AccessControlDAO

_T = TypeVar("_T")


def is_authorized_server() -> Callable[[_T], _T]:
    """Check if the server has been authorized by owner.

    Returns
    -------
    Callable[[_T], _T]
        A decorator checks whether the server is listed in the
        environment variable `AUTHORIZED_SERVER_IDS`.

    """

    def predicate(interaction: Interaction) -> bool:
        return interaction.guild_id in AUTHORIZED_SERVER_IDS

    return app_commands.check(predicate)


def is_admin_user() -> Callable[[_T], _T]:
    """Check if the user has administrative access permission.

    Returns
    -------
    Callable[[_T], _T]
        A decorator checks whether the user executing command is listed
        in the environment variable `ADMIN_USER_IDS`.

    """

    def predicate(interaction: Interaction) -> bool:
        return interaction.user.id in ADMIN_USER_IDS

    return app_commands.check(predicate)


def is_advanced_user() -> Callable[[_T], _T]:
    """Check if the user has advanced access permission.

    Returns
    -------
    Callable[[_T], _T]
        A decorator checks whether the user executing command is listed
        in the table `access_control` with the access type `advanced`.

    """

    async def predicate(interaction: Interaction) -> bool:
        advanced_user_ids = await AccessControlDAO().fetch_user_ids_by_access_type(
            access_type="advanced"
        )
        return interaction.user.id in advanced_user_ids

    return app_commands.check(predicate)


def is_not_blocked_user() -> Callable[[_T], _T]:
    """Check if user has not been blocked.

    Returns
    -------
    Callable[[_T], _T]
        A decorator checks whether the user executing command is not
        listed in the table `access_control` with the access type
        `blocked`.

    """

    async def predicate(interaction: Interaction) -> bool:
        blocked_user_ids = await AccessControlDAO().fetch_user_ids_by_access_type(
            access_type="blocked"
        )
        return interaction.user.id not in blocked_user_ids

    return app_commands.check(predicate)
