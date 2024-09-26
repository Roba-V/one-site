from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel

from backend.models.mixins.time_stamp_mixin import TimeStampMixin


class UserBase(SQLModel, TimeStampMixin):
    """Base user model."""

    username: Optional[str] = Field(None, max_length=32, description="User name")
    firstname: Optional[str]
    lastname: Optional[str]
    nickname: Optional[str]
    email: Optional[str]


class User(UserBase, table=True):  # type: ignore
    """User DB model."""

    __tablename__ = "users"

    id: UUID = Field(default_factory=UUID, primary_key=True)
    password: Optional[str] = Field(None, max_length=128, description="User password")
    is_disabled: bool = Field(False, description="User disabled flag")
    is_superuser: bool = Field(False, description="Superuser flag")
