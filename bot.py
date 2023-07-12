import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.config import Config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.middlewares.db import DbMiddleware

from tgbot.misc.environment import Environment
from tgbot.services.database import create_db_session

logger = logging.getLogger(__name__)


def register_all_middlewares(dp: Dispatcher, config: Config, env: Environment):
    register_env_middleware(dp, env)  # must be first
    register_db_middleware(dp, env)


def register_db_middleware(dp: Dispatcher, env: Environment):
    dp.setup_middleware(DbMiddleware())


def register_env_middleware(dp: Dispatcher, env: Environment):
    dp.setup_middleware(EnvironmentMiddleware(env=env))


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp: Dispatcher):
    register_admin(dp)
    register_user(dp)
    register_echo(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(bot, storage=storage)

    env = Environment(config=config, db_session=await create_db_session(config=config))

    register_all_middlewares(dp, config, env)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = bot.session
        if session is not None:
            await session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
