from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from tgbot.services.db_base import Base
from tgbot.config import Config


AsyncSessionMaker = async_sessionmaker[AsyncSession]


async def create_db_session(config: Config) -> AsyncSessionMaker:
    
    engine = create_async_engine(
        config.db.db_url,
        echo=True,
    )

    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    
    return async_session