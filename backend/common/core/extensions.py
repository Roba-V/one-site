from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from backend.common import constants as cst
from backend.common import messages as msg
from backend.common.core.config import config
from backend.common.core.log import logger
from backend.models.user import User  # noqa: F401

logger.debug(msg.D_API_CFG_LOADED % config)
logger.debug("Initialisation process completed.")

engine = create_engine(str(config.db_uri), echo=True)
async_engine = create_async_engine(str(config.async_db_uri), echo=True, future=True)
async_session = sessionmaker(  # type: ignore
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get a database session with async.

    Returns
    -------
    AsyncGenerator[AsyncSession, None]
    """

    async with async_session() as session:
        yield session


def init_db() -> None:
    """Initialize database connection."""

    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def init_app(app: FastAPI) -> None:
    """
    Initialize API.

    Parameters
    ----------
    app: FastAPI
        instance of FastAPI
    """

    # setting CORS
    if config.API_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,  # type: ignore
            allow_origins=[
                str(origin).strip("/") for origin in config.API_CORS_ORIGINS
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Pre-processing and Post-processing of API.

    Parameters
    ----------
    _app: FastAPI
        instance of FastAPI
    -------
    """
    logger.info("startup event")
    init_db()
    yield
    logger.info("shutdown event")


# Initialize OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=cst.PATH_LOGIN[1:])
