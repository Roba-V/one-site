from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.common import constants as cst
from backend.common.core.config import config
from backend.common.core.extensions import get_async_db
from backend.common.exceptions import UnauthorizedHttpError
from backend.models import Token, User


async def authenticate_user(
    username: str, password: str, session: AsyncSession = Depends(get_async_db)
) -> bool | User:
    statement = select(User).where(User.username == username)
    result = await session.exec(statement)  # noqa
    user = result.one_or_none()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not user or not pwd_context.verify(password, user.password):
        return False
    else:
        return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=cst.JWT_ALGORITHM)
    return encoded_jwt


router = APIRouter()


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_db),
) -> Token:
    """
    Authentication API.

    Parameters
    ----------
    form_data
    session

    Returns
    -------
    """

    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise UnauthorizedHttpError()
    access_token = create_access_token(
        data={"sub": {"username": user.username}},  # type: ignore
        expires_delta=timedelta(minutes=config.API_TOKEN_EXPIRE_MINUTES),
    )

    return Token(access_token=access_token, token_type="bearer")
