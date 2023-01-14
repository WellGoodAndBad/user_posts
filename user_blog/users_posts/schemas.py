from uuid import UUID

from pydantic import constr

from user_blog.models import schemas


class CreateUserPost(schemas.CustomBaseModel):
    text_post: constr(max_length=5000)


class LikeUserPost(schemas.CustomBaseModel):
    like: bool


class AllPosts(CreateUserPost):
    post_id: UUID
