import asyncio
from uuid import UUID

import sqlalchemy.sql as sa
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from user_blog.common import database
from user_blog.models import models as md


async def insert_user_post(user_id: UUID,
                           text_post: str) -> None:
    values = {
        "user_id": str(user_id),
        "text_post": text_post
    }
    stmt = sa.insert(md.UserPost) \
        .values(values)

    async with database.session() as ses:
        return await ses.execute(stmt)


async def is_owner_post(user_id: UUID,
                        post_id: UUID) -> bool:
    stmt = sa.select([md.UserPost.c.user_id])\
        .where(md.UserPost.c.post_id == str(post_id))

    async with database.session() as ses:
        if await ses.scalar(stmt) == str(user_id):
            return True
        return False


async def delete_user_post(post_id: UUID) -> None:
    stmt = sa.delete(md.UserPost) \
        .where(md.UserPost.c.post_id == str(post_id))

    async with database.session() as ses:
        return await ses.execute(stmt)


async def update_user_post(post_id: UUID,
                           user_id: UUID,
                           text_post: str) -> None:
    values = {
        "text_post": text_post,
    }

    stmt = md.UserPost \
        .update().values(values) \
        .where(md.UserPost.c.post_id == str(post_id))\
        .where(md.UserPost.c.user_id == str(user_id))

    async with database.session() as ses:
        return await ses.execute(stmt)


async def _add_value_like(user_id: UUID,
                          post_id: UUID,
                          value: dict[str, bool],
                          conn: AsyncSession) -> None:
    values = {
        "user_id": str(user_id),
        "post_id": str(post_id),
        **value
    }

    stmt = sa.insert(md.LikeUserPost) \
        .values(values)

    await conn.execute(stmt)


async def _get_count_likes(post_id: UUID) -> int:
    stmt = sa.select(sa.func.count(1))\
            .select_from(md.LikeUserPost) \
            .where(md.LikeUserPost.c.likes == True) \
            .where(md.LikeUserPost.c.post_id == str(post_id))

    async with database.session() as ses:
        if (count := await ses.scalar(stmt)) is None:
            return -1
        return count


async def _get_count_dislikes(post_id: UUID) -> int:
    stmt = sa.select(sa.func.count(1))\
            .select_from(md.LikeUserPost) \
            .where(md.LikeUserPost.c.likes == False) \
            .where(md.LikeUserPost.c.post_id == str(post_id))
    async with database.session() as ses:
        if (count := await ses.scalar(stmt)) is None:
            return -1
        return count


async def get_count_dis_likes(post_id: UUID) -> dict[str, int]:
    count_likes = asyncio.create_task(_get_count_likes(post_id=post_id))
    count_dis = asyncio.create_task(_get_count_dislikes(post_id=post_id))

    await asyncio.gather(
        count_likes,
        count_dis
    )
    return {
        "likes": count_likes.result(),
        "dislikes": count_dis.result()
    }


async def add_like_user_post(post_id: UUID,
                             user_id: UUID,
                             like: bool) -> None:
    async with database.session() as ses:
        if like:
            await _add_value_like(user_id=user_id,
                                  post_id=post_id,
                                  value={"likes": True},
                                  conn=ses)
        else:
            await _add_value_like(user_id=user_id,
                                  post_id=post_id,
                                  value={"likes": False},
                                  conn=ses)


async def get_all_posts() -> list[RowMapping]:
    stmt = sa.select([md.UserPost.c.post_id,
                      md.UserPost.c.text_post])

    async with database.session() as ses:
        return (await ses.execute(stmt)).mappings().all()


async def is_liked(user_id: UUID,
                   post_id: UUID) -> bool:
    stmt = sa.select(sa.func.count(1) > 0)\
        .select_from(md.LikeUserPost)\
        .where(md.LikeUserPost.c.user_id == str(user_id))\
        .where(md.LikeUserPost.c.post_id == str(post_id))

    async with database.session() as ses:
        return await ses.scalar(stmt)


async def update_like(post_id: UUID,
                      user_id: UUID,
                      like: bool) -> None:
    values = {
        "likes": like,
    }

    stmt = md.LikeUserPost \
        .update().values(values) \
        .where(md.LikeUserPost.c.post_id == str(post_id))\
        .where(md.LikeUserPost.c.user_id == str(user_id))

    async with database.session() as ses:
        return await ses.execute(stmt)