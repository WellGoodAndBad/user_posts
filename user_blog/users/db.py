from uuid import UUID

import sqlalchemy.sql as sa

from user_blog.common import database
from user_blog.models import models as md


async def insert_user(login: str,
                      password: str) -> UUID:
    values = {
        "login": login,
        "password": password
    }
    stmt = sa.insert(md.Users) \
        .values(values) \
        .returning(md.Users.c.user_id)

    async with database.session() as ses:
        return await ses.scalar(stmt)


async def is_login_unique(login: str) -> bool:
    stmt = sa.select(sa.func.count(1) == 0)\
        .select_from(md.Users)\
        .where(md.Users.c.login == login)

    async with database.session() as ses:
        return await ses.scalar(stmt)
