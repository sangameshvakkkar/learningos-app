from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LessonProgressRead(BaseModel):
    id: UUID
    lesson_id: UUID
    completed_at: datetime

    model_config = ConfigDict(from_attributes=True)
