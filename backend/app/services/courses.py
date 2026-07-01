from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import User
from app.schemas.course import CourseCreate


def list_courses(db: Session) -> list[Course]:
    return list(db.scalars(select(Course).order_by(Course.title)))


def get_course(db: Session, course_id: UUID) -> Course | None:
    return db.get(Course, course_id)


def create_course(db: Session, payload: CourseCreate) -> Course:
    course = Course(**payload.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def enroll_user(db: Session, user: User, course: Course) -> Enrollment:
    existing = db.scalar(
        select(Enrollment).where(Enrollment.user_id == user.id, Enrollment.course_id == course.id)
    )
    if existing:
        return existing
    enrollment = Enrollment(user_id=user.id, course_id=course.id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


def list_user_enrollments(db: Session, user: User) -> list[Enrollment]:
    statement = (
        select(Enrollment)
        .options(joinedload(Enrollment.course))
        .where(Enrollment.user_id == user.id)
        .order_by(Enrollment.enrolled_at.desc())
    )
    return list(db.scalars(statement))
