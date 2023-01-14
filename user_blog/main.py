#!/usr/bin/env python3

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from user_blog.common import database
from user_blog.users import routes as user_routes
from user_blog.users_posts import routes as post_routes

app = FastAPI(
    title="Users Posts",
)

app.include_router(user_routes.router)
app.include_router(post_routes.router)


@app.exception_handler(database.DatabaseError)
async def database_exception_handler(request: Request,
                                     exc: database.DatabaseError):
    # need logger here

    return ORJSONResponse(
        content={'detail': 'Internal server error'},
        status_code=500
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request,
                                       exc: RequestValidationError):
    # need logger here

    return ORJSONResponse(
        content={'detail': exc.json()},
        status_code=422
    )


if __name__ == '__main__':
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
    )
