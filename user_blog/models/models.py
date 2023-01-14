import uuid

import sqlalchemy
from sqlalchemy import (
    MetaData,
    Table,
    Unicode,
    Boolean,
    Column, Text,
)
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()


def ForeignKey(*args, **kwargs) -> sqlalchemy.ForeignKey:
    kwargs["onupdate"] = kwargs.get("onupdate", "CASCADE")
    kwargs["ondelete"] = kwargs.get("ondelete", "RESTRICT")

    return sqlalchemy.ForeignKey(*args, **kwargs)


def PrimaryKey(*args, **kwargs) -> sqlalchemy.Column:
    if len(args) == 1:
        args = *args, UUID

    kwargs["default"] = kwargs.get("default", _uuid_gen)
    kwargs["primary_key"] = True

    return Column(*args, **kwargs)


def _uuid_gen():
    return str(uuid.uuid4())


Users = Table(
    'users',
    metadata,
    PrimaryKey('user_id', comment='ID пользователя'),
    Column('login', Unicode, index=True),
    Column('password', Unicode(255), comment='Хэш пароля'),
)


UserPost = Table(
    'user_post',
    metadata,

    PrimaryKey('post_id'),
    Column('user_id', ForeignKey('users.user_id'), nullable=False),
    Column('text_post', Text, nullable=False),
    Column('like_id', ForeignKey('like_user_post.like_id')),
)


LikeUserPost = Table(
    'like_user_post',
    metadata,

    PrimaryKey('like_id'),
    Column('user_id', ForeignKey('users.user_id'), nullable=False),
    Column('post_id', ForeignKey('user_post.post_id'), nullable=False),
    Column('likes', Boolean),
)
