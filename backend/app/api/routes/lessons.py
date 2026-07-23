from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, DbSession
from app.schemas.lesson import LessonCreate, LessonRead
from app.schemas.lesson_progress import LessonProgressRead
from app.services.courses import get_course
from app.services.lessons import (
    create_lesson,
    get_lesson,
    get_user_progress_for_course,
    list_lessons_for_course,
    mark_lesson_complete,
    get_all_user_progress,
)

router = APIRouter()


@router.get("/{course_id}/lessons", response_model=list[LessonRead])
def read_lessons(course_id: UUID, db: DbSession) -> list[LessonRead]:
    course = get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return list_lessons_for_course(db, course_id)


@router.get("/{course_id}/lessons/{lesson_id}", response_model=LessonRead)
def read_lesson(course_id: UUID, lesson_id: UUID, db: DbSession) -> LessonRead:
    lesson = get_lesson(db, lesson_id)
    if not lesson or lesson.course_id != course_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    return lesson


@router.post("/{course_id}/lessons", response_model=LessonRead, status_code=status.HTTP_201_CREATED)
def add_lesson(course_id: UUID, payload: LessonCreate, db: DbSession, current_user: CurrentUser) -> LessonRead:
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    course = get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return create_lesson(db, course_id, payload)


@router.post("/{course_id}/lessons/{lesson_id}/complete", response_model=LessonProgressRead)
def complete_lesson(course_id: UUID, lesson_id: UUID, db: DbSession, current_user: CurrentUser) -> LessonProgressRead:
    lesson = get_lesson(db, lesson_id)
    if not lesson or lesson.course_id != course_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    return mark_lesson_complete(db, current_user, lesson_id)


@router.get("/{course_id}/progress", response_model=list[LessonProgressRead])
def course_progress(course_id: UUID, db: DbSession, current_user: CurrentUser) -> list[LessonProgressRead]:
    return get_user_progress_for_course(db, current_user, course_id)


@router.get("/me/progress", response_model=list[LessonProgressRead])
def all_progress(db: DbSession, current_user: CurrentUser) -> list[LessonProgressRead]:
    return get_all_user_progress(db, current_user)
