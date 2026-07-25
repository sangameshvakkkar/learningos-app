from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.models.lesson_progress import LessonProgress
from app.models.user import User
from app.schemas.lesson import LessonCreate


def list_lessons_for_course(db: Session, course_id: UUID) -> list[Lesson]:
    return list(
        db.scalars(
            select(Lesson)
            .where(Lesson.course_id == course_id)
            .order_by(Lesson.order_index)
        )
    )


def get_lesson(db: Session, lesson_id: UUID) -> Lesson | None:
    return db.get(Lesson, lesson_id)


def get_lesson_by_slug(db: Session, course_id: UUID, lesson_slug: str) -> Lesson | None:
    return db.scalar(
        select(Lesson).where(Lesson.course_id == course_id, Lesson.slug == lesson_slug)
    )


def create_lesson(db: Session, course_id: UUID, payload: LessonCreate) -> Lesson:
    lesson = Lesson(course_id=course_id, **payload.model_dump())
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


def mark_lesson_complete(db: Session, user: User, lesson_id: UUID) -> LessonProgress:
    existing = db.scalar(
        select(LessonProgress).where(
            LessonProgress.user_id == user.id, LessonProgress.lesson_id == lesson_id
        )
    )
    if existing:
        return existing
    progress = LessonProgress(user_id=user.id, lesson_id=lesson_id)
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress


def get_user_progress_for_course(db: Session, user: User, course_id: UUID) -> list[LessonProgress]:
    return list(
        db.scalars(
            select(LessonProgress)
            .join(Lesson)
            .where(LessonProgress.user_id == user.id, Lesson.course_id == course_id)
        )
    )


def get_all_user_progress(db: Session, user: User) -> list[LessonProgress]:
    return list(db.scalars(select(LessonProgress).where(LessonProgress.user_id == user.id)))
