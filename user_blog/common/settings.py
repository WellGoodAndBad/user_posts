import os

from environs import Env

env = Env()
env.read_env()

DSN_TEMPLATE = 'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}'

with env.prefixed('DB_'):
    DB_HOST = env('HOST')
    DB_PORT = env.int('PORT', 5432)
    DB_USERNAME = env('USERNAME')
    DB_PASSWORD = env('PASSWORD')
    DB_NAME = env('NAME')

    DB_DSN = DSN_TEMPLATE.format(
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        db_name=DB_NAME
    )

with env.prefixed('API_'):
    API_SECRET_KEY = env("SECRET_KEY")
    API_TOKEN_LIFETIME = env.int('TOKEN_LIFETIME', 1_440)
    API_ALGORITHM = env('ALGORITHM', 'HS256')

with env.prefixed('REDIS_'):
    REDIS_HOST = env('HOST')

os.environ.clear()
