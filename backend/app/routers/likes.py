from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..dependencies import get_db, get_current_user
from ..crud.crud import like_post
from ..schemas.schemas import LikeOut
from ..models.models import User

router = APIRouter(
    prefix="/api/likes",
    tags=["likes"]
)

@router.post("/", response_model=LikeOut)
def like_a_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    liked = like_post(db, post_id, current_user.id)
    return liked
