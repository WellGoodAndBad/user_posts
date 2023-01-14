import datetime
import os
from typing import Union, Literal

import argon2
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from user_blog.common import settings
from user_blog.auth import db, schemas


SECRET_KEY = settings.API_SECRET_KEY
ALGORITHM = settings.API_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.API_TOKEN_LIFETIME

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
RESPONSES = {
    401: {'description': "Could not validate credentials"},
}
ph = argon2.PasswordHasher(
    parallelism=2 * (os.cpu_count() or 1),
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


def get_hash(*,
             plain_password: str) -> str:
    return ph.hash(plain_password)


async def _verify_pwd(login: str,
                      password: str) -> Union[str, bool]:
    if (user := await db.get_user(login=login)) is None:
        return False
    pwd_hash = user.password

    try:
        ph.verify(pwd_hash, password)
    except (argon2.exceptions.VerifyMismatchError,
            argon2.exceptions.VerificationError):
        pass  # need logger here
    except argon2.exceptions.InvalidHash:
        pass  # need logger here
    else:
        return pwd_hash
    return False


async def verify_pwd(login: str,
                     password: str) -> bool:
    if (pwd_hash := await _verify_pwd(login, password)) is False:
        return False

    if ph.check_needs_rehash(pwd_hash):
        hashed_pwd = ph.hash(password)
        await db.update_password(login=login, hashed_pwd=hashed_pwd)
    return True


async def authenticate_user(login: str,
                            password: str) -> Union[schemas.User, Literal[False]]:
    if (user := await db.get_user(login=login)) is None:
        return False
    if not await verify_pwd(login, password):
        return False
    return user


def create_access_token(login: str,
                        expires_delta: int = None) -> str:
    delta = expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=delta)

    to_encode = {
        "sub": login,
        "exp": expire
    }

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> schemas.User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        if (login := payload.get("sub")) is None:
            raise CREDENTIALS_EXCEPTION
    except JWTError:
        raise CREDENTIALS_EXCEPTION

    if (user := await db.get_user(login=login)) is None:
        raise CREDENTIALS_EXCEPTION
    return user
