from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from tgbot.misc.environment import Environment
from aiogram import types
from tgbot.models.user import User


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    async def pre_process(self, obj, data, *args):
        env: Environment = obj.env
        telegram_user: types.User = obj.from_user
        user = await User.get_user(
            session_maker=env.db_session, telegram_id=telegram_user.id
        )
        if user is None:
            user = await User.add_user(
                session_maker=env.db_session,
                telegram_id=telegram_user.id,
                telegram_username=telegram_user.username,
            )
        obj.from_user.user_model = user
