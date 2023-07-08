from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from tgbot.misc.environment import Environment
from aiogram import types

class DbMiddleware(LifetimeControllerMiddleware):
    
    async def pre_process(self, obj, data, *args):
        env:Environment = data["env"]
        telegram_user: types.User = obj.from_user
        user = await User.get_user(session_maker=session_maker, telegram_id=telegram_user.id)
        

        data['user'] = user