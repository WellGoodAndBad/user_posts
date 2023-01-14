from pydantic import constr

from user_blog.models import schemas


class User(schemas.CustomBaseModel):
    login: constr(max_length=50)
    password: constr(max_length=50)


