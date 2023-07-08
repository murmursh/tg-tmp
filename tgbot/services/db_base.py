from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(AsyncAttrs, DeclarativeBase):
    pass