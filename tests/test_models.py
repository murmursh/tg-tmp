from tgbot.models.user import User, Roles
from faker import Faker
from tgbot.config import load_config
from tgbot.services.database import create_db_session
from pathlib import Path
from sqlalchemy.exc import IntegrityError

import asyncio
import pytest


class TestUser:
    def test_add_user(self, tmp_path: Path):
        async def test():
            fake = Faker()

            config = load_config(".env")
            config.db.db_url = f"sqlite+aiosqlite:///{tmp_path}/test_add_user.db"
            session_maker = await create_db_session(config)

            ids = [fake.unique.random_number(digits=10) for _ in range(1, 101)]
            names = [fake.first_name() for _ in range(1, 10)]

            for user_id, first_name in zip(ids, names):
                user = await User.add_user(session_maker, user_id, first_name)
                # user = await User.get_user(session, user_id)
                assert user is not None
                assert user.telegram_id == user_id
                assert user.telegram_username == first_name

        asyncio.run(test())

    def test_add_user_not_unique_id(self, tmp_path: Path):
        async def test():
            fake = Faker()
            config = load_config(".env")
            config.db.db_url = f"sqlite+aiosqlite:///{tmp_path}/test_unique_id.db"
            session_maker = await create_db_session(config)

            ids = [fake.unique.random_number(digits=10) for _ in range(1, 10)]
            names = [fake.first_name() for _ in range(1, 10)]

            for user_id, first_name in zip(ids, names):
                user = await User.add_user(session_maker, user_id, first_name)
                assert user is not None
                assert user.telegram_id == user_id
                assert user.telegram_username == first_name

            for user_id, first_name in zip(ids, names):
                try:
                    user = await User.add_user(session_maker, user_id, first_name)
                except Exception as e:
                    assert IntegrityError == type(e)

        asyncio.run(test())

    def test_get_user(self, tmp_path: Path):
        async def test():
            fake = Faker()
            config = load_config(".env")
            config.db.db_url = f"sqlite+aiosqlite:///{tmp_path}/test_get_user.db"
            session_maker = await create_db_session(config)

            ids = [fake.unique.random_number(digits=10) for _ in range(1, 10)]
            names = [fake.first_name() for _ in range(1, 10)]

            for user_id, first_name in zip(ids, names):
                user = await User.add_user(session_maker, user_id, first_name)
                assert user is not None
                assert user.telegram_id == user_id
                assert user.telegram_username == first_name

            for user_id, first_name in zip(ids, names):
                user = await User.get_user(session_maker, user_id)
                assert user is not None
                assert user.telegram_id == user_id
                assert user.telegram_username == first_name

        asyncio.run(test())

    def test_get_user_not_found(self, tmp_path: Path):
        async def test():
            fake = Faker()
            config = load_config(".env")
            config.db.db_url = (
                f"sqlite+aiosqlite:///{tmp_path}/test_get_user_not_found.db"
            )
            session_maker = await create_db_session(config)

            ids = [fake.unique.random_number(digits=10) for _ in range(1, 10)]
            names = [fake.first_name() for _ in range(1, 10)]

            for user_id, first_name in zip(ids, names):
                user = await User.add_user(session_maker, user_id, first_name)
                assert user is not None
                assert user.telegram_id == user_id
                assert user.telegram_username == first_name

            for user_id, first_name in zip(ids, names):
                user = await User.get_user(
                    session_maker, fake.unique.random_number(digits=11)
                )
                assert user is None

        asyncio.run(test())

    def test_update_username(self, tmp_path: Path):
        async def test():
            fake = Faker()
            config = load_config(".env")
            config.db.db_url = f"sqlite+aiosqlite:///{tmp_path}/test_update_username.db"
            session_maker = await create_db_session(config)

            ids = [fake.unique.random_number(digits=10) for _ in range(1, 10)]
            names = [fake.first_name() for _ in range(1, 10)]

            for user_id, first_name in zip(ids, names):
                user = await User.add_user(session_maker, user_id, first_name)
                assert user is not None
                assert user.telegram_id == user_id
                assert user.telegram_username == first_name

            for user_id, first_name in zip(ids, names):
                new_name = fake.first_name()
                user = await User.get_user(session_maker, user_id)
                assert user is not None
                await user.update_telegram_username(session_maker, new_name)
                assert user is not None
                assert user.telegram_username == new_name
                user = await User.get_user(session_maker, user_id)
                assert user is not None
                assert user.telegram_username == new_name

        asyncio.run(test())

    def test_permissions_field(self, tmp_path: Path):
        async def test():
            fake = Faker()
            config = load_config(".env")
            config.db.db_url = (
                f"sqlite+aiosqlite:///{tmp_path}/test_permissions_field.db"
            )
            session_maker = await create_db_session(config)
            ids = [fake.unique.random_number(digits=10) for _ in range(1, 10)]
            names = [fake.first_name() for _ in range(1, 10)]

            for user_id, first_name in zip(ids, names):
                user = await User.add_user(session_maker, user_id, first_name)
                assert user is not None
                assert user.telegram_id == user_id
                assert user.telegram_username == first_name
                assert user.role == Roles.DEFAULT

            new_role = Roles.ANON if Roles.ANON != Roles.DEFAULT else Roles.USER
            assert Roles.ANON < Roles.ADMIN
            assert not (Roles.ADMIN < Roles.ANON)

            for user_id, first_name in zip(ids, names):
                user = await User.get_user(session_maker, user_id)
                assert user is not None
                assert user.telegram_id == user_id
                assert user.telegram_username == first_name
                assert user.role == Roles.DEFAULT
                await user.update_role(session_maker, new_role)
                assert user.role == new_role

            for user_id, first_name in zip(ids, names):
                user = await User.get_user(session_maker, user_id)
                assert user is not None
                assert user.telegram_id == user_id
                assert user.telegram_username == first_name
                assert user.role == new_role

        asyncio.run(test())
