import datetime

from tgbot.services.database import Base, AsyncSessionMaker

from typing import Optional, Any
from enum import Enum

from sqlalchemy import func, insert, select, update
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


# todo mobe Enum to types
class Roles(Enum):
    DEFAULT = 4
    ANON = 0
    USER = 1
    MODERATOR = 2
    ADMIN = 3

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented


# AsyncSessionMaker == async_sessionmaker[AsyncSession]
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    create_date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    telegram_id: Mapped[int] = mapped_column(unique=True)
    telegram_username: Mapped[str]
    role: Mapped[Roles] = mapped_column(server_default=Roles.DEFAULT.name)

    @classmethod
    async def add_user(
        cls, session_maker: AsyncSessionMaker, telegram_id: int, telegram_username: str
    ) -> Optional["User"]:
        insert_sql = (
            insert(cls)
            .values(telegram_id=telegram_id, telegram_username=telegram_username)
            .returning(cls)
        )
        async with session_maker() as ses:
            result = await ses.execute(insert_sql)
            await ses.commit()
        return result.scalar()

    @classmethod
    async def get_user(
        cls, session_maker: AsyncSessionMaker, telegram_id: int
    ) -> Optional["User"]:
        select_sql = select(cls).where(cls.telegram_id == telegram_id)
        async with session_maker() as ses:
            result = await ses.execute(select_sql)
            await ses.commit()
        return result.scalar()

    async def _update_user(self, session_maker: AsyncSessionMaker, **kwargs) -> Any:
        update_sql = (
            update(User).where(User.telegram_id == self.telegram_id).values(**kwargs)
        )
        async with session_maker() as ses:
            result = await ses.execute(update_sql)
            await ses.commit()
        return result

    async def update_telegram_username(
        self, session_maker: AsyncSessionMaker, telegram_username: str
    ) -> Any:
        res = await self._update_user(
            session_maker, telegram_username=telegram_username
        )
        self.telegram_username = telegram_username  # this is safe see https://stackoverflow.com/questions/76643384/sqlalchemy-object-update-after-update-sql-method
        return res

    async def update_role(self, session_maker: AsyncSessionMaker, role: Roles) -> Any:
        res = await self._update_user(session_maker, role=role)
        self.role = role
