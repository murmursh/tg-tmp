from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from tgbot.misc.environment import Environment


class EnvironmentMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]
    
    def __init__(self, env: Environment):
        super().__init__()
        self.env = env
    
    async def pre_process(self, obj, data: dict, *args):
        data.update({"env": self.env})
        
