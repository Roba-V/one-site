from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field


class TimeStampMixin(BaseModel):
    """Time stamp mixin model."""

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(
        default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}
    )
