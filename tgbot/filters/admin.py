import typing

from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import Config
from tgbot.types import Environment, User, Roles


class AdminFilter(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, obj):
        if self.is_admin is None:
            return False
        user = obj.from_user.user_model
        return user and user.role >= Roles.ADMIN
