from dataclasses import dataclass
from tgbot.config import Config
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class Environment:
    config:Config
    db_session:async_sessionmaker[AsyncSession]
    