import sqlalchemy.sql as sa

from user_blog.common import database
from user_blog.models import models as md
from user_blog.auth import schemas


async def update_password(login: str,
                          hashed_pwd: str) -> None:
    stmt = md.Users.update() \
        .where(md.Users.c.login == login) \
        .values(password=hashed_pwd)\

    async with database.session() as ses:
        await ses.execute(stmt)


async def get_user(login: str) -> schemas.User:
    stmt = sa.select(md.Users) \
        .where(md.Users.c.login == login)

    async with database.session() as ses:
        if not (user := (await ses.execute(stmt)).mappings().one_or_none()):
            raise ValueError("User login=%s not found", login)

    return schemas.User(**user)
