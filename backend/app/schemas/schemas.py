from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class CommentOut(BaseModel):
    id: int
    content: str
    author: Optional[UserOut]
    created_at: datetime

    class Config:
        orm_mode = True

class PostOut(PostBase):
    id: int
    author: UserOut
    created_at: datetime
    comments: List[CommentOut] = []
    likes_count: int = 0

    class Config:
        orm_mode = True

class CommentCreate(BaseModel):
    post_id: int
    content: str

class LikeOut(BaseModel):
    id: int
    user: UserOut
    created_at: datetime

    class Config:
        orm_mode = True

# Authentication schemas
class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
