from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..dependencies import get_db, get_current_user
from ..crud.crud import get_comments_by_post, create_comment
from ..schemas.schemas import CommentOut, CommentCreate
from ..models.models import User

router = APIRouter(
    prefix="/api/comments",
    tags=["comments"]
)

@router.get("/", response_model=List[CommentOut])
def read_comments(post_id: int, db: Session = Depends(get_db)):
    comments = get_comments_by_post(db, post_id)
    return comments

@router.post("/", response_model=CommentOut)
def create_new_comment(
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = create_comment(db, comment_in, current_user.id)
    return comment
