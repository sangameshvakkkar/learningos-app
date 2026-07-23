from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LessonBase(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    slug: str = Field(min_length=3, max_length=255)
    content: str = Field(min_length=10)
    order_index: int = Field(ge=0)
    duration_minutes: int = Field(gt=0, default=10)


class LessonCreate(LessonBase):
    pass


class LessonRead(LessonBase):
    id: UUID
    course_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LessonSummary(BaseModel):
    """Lesson without full content — used in course detail listings."""

    id: UUID
    title: str
    slug: str
    order_index: int
    duration_minutes: int

    model_config = ConfigDict(from_attributes=True)
