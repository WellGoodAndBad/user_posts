from uuid import UUID

from pydantic import constr

from user_blog.models import schemas


class Token(schemas.CustomBaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: UUID


class User(schemas.CustomBaseModel):
    user_id: UUID
    login: constr(max_length=50)
    password: str
