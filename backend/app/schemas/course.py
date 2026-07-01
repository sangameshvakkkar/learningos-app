from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CourseBase(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    slug: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=10)
    level: str = Field(min_length=3, max_length=50)
    duration_minutes: int = Field(gt=0)


class CourseCreate(CourseBase):
    pass


class CourseRead(CourseBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EnrollmentRead(BaseModel):
    id: UUID
    course: CourseRead
    enrolled_at: datetime

    model_config = ConfigDict(from_attributes=True)
