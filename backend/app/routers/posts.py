from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..dependencies import get_db, get_current_user_optional
from ..crud.crud import get_posts, get_post, create_post, count_likes, get_user_by_username, delete_post
from ..schemas.schemas import PostOut, PostCreate
from ..models.models import User

router = APIRouter(
    prefix="/api/posts",
    tags=["posts"]
)

@router.get("/", response_model=List[PostOut])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = get_posts(db, skip, limit)
    result = []
    for post in posts:
        likes = count_likes(db, post.id)
        result.append(PostOut(
            id=post.id,
            title=post.title,
            content=post.content,
            author=post.author,
            created_at=post.created_at,
            comments=post.comments,
            likes_count=likes
        ))
    return result

@router.get("/{post_id}", response_model=PostOut)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    likes = count_likes(db, post.id)
    return PostOut(
        id=post.id,
        title=post.title,
        content=post.content,
        author=post.author,
        created_at=post.created_at,
        comments=post.comments,
        likes_count=likes
    )

@router.post("/", response_model=PostOut)
def create_new_post(
    post_in: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    # allow anonymous posts
    if current_user:
        author_id = current_user.id
    else:
        anon = get_user_by_username(db, 'Anonymous')
        author_id = anon.id
    post = create_post(db, post_in, author_id)
    likes = count_likes(db, post.id)
    return PostOut(
        id=post.id,
        title=post.title,
        content=post.content,
        author=post.author,
        created_at=post.created_at,
        comments=post.comments,
        likes_count=likes
    )

@router.delete("/{post_id}", status_code=204)
def delete_existing_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    """Delete a post by ID (no authentication required)"""
    success = delete_post(db, post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return Response(status_code=204)
