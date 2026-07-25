from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentUser, DbSession
from app.schemas.course import CourseCreate, CourseDetail, CourseRead, EnrollmentRead
from app.services.courses import (
    create_course,
    enroll_user,
    get_course,
    get_course_with_lessons,
    list_courses,
    list_user_enrollments,
)

router = APIRouter()


@router.get("", response_model=list[CourseRead])
def read_courses(
    db: DbSession,
    search: str | None = Query(None, min_length=1, description="Search courses by title"),
    level: str | None = Query(None, description="Filter by level"),
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(50, ge=1, le=100, description="Pagination limit"),
) -> list[CourseRead]:
    courses, _ = list_courses(db, search=search, level=level, skip=skip, limit=limit)
    return courses


@router.get("/{course_id}", response_model=CourseDetail)
def read_course(course_id: UUID, db: DbSession) -> CourseDetail:
    course = get_course_with_lessons(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course


@router.post("", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def add_course(payload: CourseCreate, db: DbSession, current_user: CurrentUser) -> CourseRead:
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return create_course(db, payload)


@router.post("/{course_id}/enroll", response_model=EnrollmentRead)
def enroll(course_id: UUID, db: DbSession, current_user: CurrentUser) -> EnrollmentRead:
    course = get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    enrollment = enroll_user(db, current_user, course)
    enrollment.course = course
    return enrollment


@router.get("/me/enrollments", response_model=list[EnrollmentRead])
def my_enrollments(db: DbSession, current_user: CurrentUser) -> list[EnrollmentRead]:
    return list_user_enrollments(db, current_user)
