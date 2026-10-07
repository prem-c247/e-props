import logging
from contextlib import asynccontextmanager
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI

# Configure logging at startup before application initialization
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        # 1. Saves to a file (auto-rotates when file reaches 5MB, keeps last 3 files)
        RotatingFileHandler("app.log", maxBytes=5_000_000, backupCount=3),
        # 2. Also prints to your terminal console
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

from app.config import settings
from app.database import Base, engine
from app.exceptions import register_exception_handlers
from app.models import (  # Register all models with Base metadata
    AmenitiesModel,
    PropertyAmenitiesModel,
    PropertyModel,
    UserModel,
)
from app.routes.v1 import router as api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-create tables in PostgreSQL on startup
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("PostgreSQL: Tables verified/created successfully.")
    except Exception as e:
        logger.warning(
            "PostgreSQL Notice: Could not connect to PostgreSQL on startup. Reason: %s",
            e,
        )
        logger.warning("-> Update your password in .env (DATABASE_URL) and restart.")
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Modular FastAPI REST API for Properties and Users backed by PostgreSQL & SQLAlchemy",
    lifespan=lifespan,
)

# Register centralized exception handlers
register_exception_handlers(app)

# Mount the unified v1 router
app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs": "/docs",
        "database": "PostgreSQL (SQLAlchemy)",
        "endpoints": {
            "properties": "/properties",
            "users": "/users",
            "api_v1": settings.API_V1_PREFIX,
        },
    }
