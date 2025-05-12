from sqlalchemy.orm import Session
from ..models.models import User, Post, Comment, Like
from ..schemas.schemas import PostCreate, CommentCreate, UserCreate
from passlib.context import CryptContext

# Users
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# Authentication helpers
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_user(db: Session, user: UserCreate):
    """Create a new user with hashed password"""
    hashed_password = get_password_hash(user.password)
    # assign a dummy email as registration no longer includes it
    email = f"{user.username}@example.com"
    db_user = User(username=user.username, email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    """Authenticate user by username and password"""
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Posts
def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def create_post(db: Session, post: PostCreate, user_id: int):
    db_post = Post(**post.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int) -> bool:
    """Delete a post by ID"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return False
    db.delete(post)
    db.commit()
    return True

# Comments
def get_comments_by_post(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).all()

def create_comment(db: Session, comment: CommentCreate, user_id: int):
    db_comment = Comment(post_id=comment.post_id, content=comment.content, author_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# Likes
def like_post(db: Session, post_id: int, user_id: int):
    existing = db.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).first()
    if existing:
        return existing
    like = Like(post_id=post_id, user_id=user_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like

def count_likes(db: Session, post_id: int):
    return db.query(Like).filter(Like.post_id == post_id).count()
