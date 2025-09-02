from fastapi import FastAPI
from .config import settings
from .dependencies import engine, SessionLocal
from .models.models import Base
from .routers import auth, posts, comments, likes
from .crud.crud import get_user_by_username, create_user
from .schemas.schemas import UserCreate
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import asyncio
import logging
from sqlalchemy.exc import OperationalError

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Containerized Blog Platform API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

@app.get("/health")
async def health():
    return {"status": "ok"}

def create_tables():
    Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def on_startup():
    # Retry logic for database initialization to avoid crashing when Postgres is not yet ready
    max_retries = 10
    delay_seconds = 3

    for attempt in range(1, max_retries + 1):
        try:
            create_tables()
            db = SessionLocal()
            try:
                if not get_user_by_username(db, 'Anonymous'):
                    create_user(db, UserCreate(username='Anonymous', password=''))
            finally:
                db.close()
            logger.info("Database ready and startup seeding complete")
            break
        except OperationalError as e:
            logger.warning(f"Database not ready (attempt {attempt}/{max_retries}): {e}")
            if attempt == max_retries:
                logger.exception("Exceeded maximum retries waiting for the database")
                raise
            await asyncio.sleep(delay_seconds)

# Register routers
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)