import jwt
from fastapi import APIRouter, Depends, HTTPException
from jwt.exceptions import InvalidTokenError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.common import constants as cst
from backend.common.core.config import config
from backend.common.core.extensions import get_async_db, oauth2_scheme
from backend.common.exceptions import UnauthorizedHttpError
from backend.models import User

router = APIRouter()


async def get_current_active_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_db)
):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[cst.JWT_ALGORITHM])
        username: str = payload.get("sub").get("username")
        if username is None:
            raise UnauthorizedHttpError()
    except InvalidTokenError:
        raise UnauthorizedHttpError()
    statement = select(User).where(User.username == username)
    result = await session.exec(statement)  # noqa
    user = result.one_or_none()
    if user is None:
        raise UnauthorizedHttpError()
    elif user.is_disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    ログイン中のユーザー取得 API．

    Parameters
    ----------
    current_user: User
        ログイン中のユーザー

    Returns
    -------
    """

    return current_user


@router.get("/ss")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    return token
