from uuid import UUID

from fastapi import APIRouter, HTTPException, Response, Depends

from user_blog import auth
from user_blog.common import redis_api
from user_blog.users_posts import db, schemas

router = APIRouter(
    prefix='/users_posts',
    tags=['users_posts'],
)


@router.post('/create_post',
             status_code=201)
async def create_new_post(post: schemas.CreateUserPost,
                          user: auth.User = Depends(auth.get_current_user)):

    await db.insert_user_post(
        user_id=user.user_id,
        text_post=post.text_post
    )

    return Response(status_code=201)


@router.delete('/delete_post',
               status_code=204)
async def create_new_post(post_id: UUID,
                          user: auth.User = Depends(auth.get_current_user)):
    if not await db.is_owner_post(user_id=user.user_id,
                                  post_id=post_id):
        raise HTTPException(status_code=403, detail="user is not owner")

    await db.delete_user_post(
        post_id=post_id
    )


@router.put('/update_post',
            status_code=200)
async def create_new_post(post_id: UUID,
                          post: schemas.CreateUserPost,
                          user: auth.User = Depends(auth.get_current_user)):
    if not await db.is_owner_post(user_id=user.user_id,
                                  post_id=post_id):
        raise HTTPException(status_code=403, detail="user is not owner")

    await db.update_user_post(
        post_id=post_id,
        text_post=post.text_post,
        user_id=user.user_id
        )

    return Response(status_code=200)


@router.post('/like_post',
             status_code=201)
async def add_like_user_post(post_id: UUID,
                             user: auth.User = Depends(auth.get_current_user)):
    if await db.is_owner_post(user_id=user.user_id,
                              post_id=post_id):
        raise HTTPException(status_code=403, detail="user can't like it, cause owner")
    if await db.is_liked(user_id=user.user_id,
                         post_id=post_id):
        await db.update_like(user_id=user.user_id,
                             post_id=post_id,
                             like=True)

        count = await db.get_count_dis_likes(post_id=post_id)
        await redis_api.add_likes_dislikes(post_id=post_id, likes_dislikes=count)

        return Response(status_code=201)

    await db.add_like_user_post(
        user_id=user.user_id,
        post_id=post_id,
        like=True,
    )

    count = await db.get_count_dis_likes(post_id=post_id)
    await redis_api.add_likes_dislikes(post_id=post_id, likes_dislikes=count)

    return Response(status_code=201)


@router.post('/dislike_post',
             status_code=201)
async def add_like_user_post(post_id: UUID,
                             user: auth.User = Depends(auth.get_current_user)):
    if await db.is_owner_post(user_id=user.user_id,
                              post_id=post_id):
        raise HTTPException(status_code=403, detail="user can't dislike it, cause owner")
    if await db.is_liked(user_id=user.user_id,
                         post_id=post_id):
        await db.update_like(user_id=user.user_id,
                             post_id=post_id,
                             like=False)
        count = await db.get_count_dis_likes(post_id=post_id)
        await redis_api.add_likes_dislikes(post_id=post_id, likes_dislikes=count)

        return Response(status_code=201)
    await db.add_like_user_post(
        user_id=user.user_id,
        post_id=post_id,
        like=False
    )
    count = await db.get_count_dis_likes(post_id=post_id)
    await redis_api.add_likes_dislikes(post_id=post_id, likes_dislikes=count)

    return Response(status_code=201)


@router.get('/all_post',
            response_model=list[schemas.AllPosts],
            status_code=200)
async def get_all_post():

    return await db.get_all_posts()


@router.get('/post_dis_likes',
            response_model=dict[str, int],
            status_code=200)
async def get_count_like_and_dislike(post_id: UUID):

    return await redis_api.get_likes_dislikes(post_id=post_id)
