from fastapi import APIRouter, HTTPException, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm

from user_blog import auth
from user_blog.users import db, schemas

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.post('/register',
             status_code=201)
async def register_new_user(user: schemas.User):
    if not await db.is_login_unique(login=user.login):
        raise HTTPException(status_code=400, detail="login not unique")

    hashed_password = auth.get_hash(plain_password=user.password)

    await db.insert_user(
        login=user.login,
        password=hashed_password
    )

    return Response(status_code=201)


@router.post('/token',
             response_model=auth.Token)
async def get_token(form: OAuth2PasswordRequestForm = Depends()):
    login, password = form.username, form.password

    if (user := await auth.authenticate_user(login, password)) is False:
        raise auth.CREDENTIALS_EXCEPTION

    return {
        "access_token": auth.create_access_token(user.login),
        "user_id": user.user_id
    }
