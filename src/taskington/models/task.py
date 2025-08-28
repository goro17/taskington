"""Models used to represent tasks."""

import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


def generate_uuid():
    """Generate a unique UUID for a task."""
    return str(uuid.uuid4())


class TaskBase(SQLModel):
    """Base model for task data."""

    title: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    priority: int = Field(default=1, ge=1, le=5)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """Database model for tasks."""

    id: str = Field(default_factory=generate_uuid, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})


class TaskCreate(TaskBase):
    """Model for creating a new task."""

    pass


class TaskRead(TaskBase):
    """Model for reading tasks."""

    id: str
    created_at: datetime
    updated_at: datetime


class TaskUpdate(TaskBase):
    """Model for updating tasks."""

    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    completed: Optional[bool] = None
