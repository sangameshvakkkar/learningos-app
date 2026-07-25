from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.lesson import Lesson
from app.models.user import User
from app.schemas.course import CourseCreate


def list_courses(
    db: Session,
    *,
    search: str | None = None,
    level: str | None = None,
    skip: int = 0,
    limit: int = 50,
) -> tuple[list[dict], int]:
    """Return courses with computed lessons_count and total count for pagination."""
    query = (
        select(
            Course,
            func.count(Lesson.id).label("lessons_count"),
        )
        .outerjoin(Lesson, Lesson.course_id == Course.id)
        .group_by(Course.id)
    )

    if search:
        query = query.where(Course.title.ilike(f"%{search}%"))
    if level:
        query = query.where(Course.level == level)

    # Count total matching before pagination
    count_query = select(func.count()).select_from(Course)
    if search:
        count_query = count_query.where(Course.title.ilike(f"%{search}%"))
    if level:
        count_query = count_query.where(Course.level == level)
    total = db.scalar(count_query) or 0

    query = query.order_by(Course.title).offset(skip).limit(limit)
    rows = db.execute(query).all()

    results = []
    for course, lessons_count in rows:
        course.lessons_count = lessons_count
        results.append(course)

    return results, total


def get_course(db: Session, course_id: UUID) -> Course | None:
    return db.get(Course, course_id)


def get_course_with_lessons(db: Session, course_id: UUID) -> Course | None:
    course = db.scalar(
        select(Course).options(joinedload(Course.lessons)).where(Course.id == course_id)
    )
    if course:
        course.lessons_count = len(course.lessons)
    return course


def get_course_by_slug(db: Session, slug: str) -> Course | None:
    return db.scalar(select(Course).where(Course.slug == slug))


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
