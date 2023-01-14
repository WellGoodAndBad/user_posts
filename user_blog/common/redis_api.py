from uuid import UUID

import orjson
from redis import asyncio as aioredis

from user_blog.common import settings


class RedisException(Exception):
    pass


redis_db = aioredis.from_url(
    settings.REDIS_HOST,
    db=0, decode_responses=True)


async def add_likes_dislikes(post_id: UUID,
                             likes_dislikes: dict[str, int]) -> None:

    _json = orjson.dumps(likes_dislikes)
    await redis_db.set(str(post_id), _json)


async def get_likes_dislikes(post_id: UUID) -> dict[str, int]:
    count = await redis_db.get(str(post_id))
    return orjson.loads(count)
