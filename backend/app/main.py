from fastapi import FastAPI
from .config import settings
from .dependencies import engine, SessionLocal
from .models.models import Base
from .routers import auth, posts, comments, likes
from .crud.crud import get_user_by_username, create_user
from .schemas.schemas import UserCreate
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Containerized Blog Platform API"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instrumentation
Instrumentator().instrument(app).expose(app)

# Initialize database tables
def create_tables():
    Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def on_startup():
    create_tables()
    # ensure anonymous user exists
    db = SessionLocal()
    try:
        if not get_user_by_username(db, 'Anonymous'):
            create_user(db, UserCreate(username='Anonymous', password=''))
    finally:
        db.close()

# Register routers
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)
