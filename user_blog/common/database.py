
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.ddl import DropTable

from user_blog.common import settings
from user_blog.models import models


class DatabaseError(Exception):
    pass


engine = create_async_engine(
    settings.DB_DSN,
)


@asynccontextmanager
async def session(**kwargs) -> AsyncGenerator[AsyncSession, None]:
    new_session = AsyncSession(bind=engine, **kwargs)
    try:
        yield new_session
        await new_session.commit()
    except Exception as error:
        await new_session.rollback()

        raise DatabaseError(error) from error
    finally:
        await new_session.close()


@asynccontextmanager
async def transaction(**kwargs) -> AsyncGenerator[AsyncSession, None]:
    async with session(**kwargs) as ses:
        async with ses.begin():
            yield ses

