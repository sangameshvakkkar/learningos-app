from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, DbSession
from app.schemas.course import CourseCreate, CourseRead, EnrollmentRead
from app.services.courses import (
    create_course,
    enroll_user,
    get_course,
    list_courses,
    list_user_enrollments,
)

router = APIRouter()


@router.get("", response_model=list[CourseRead])
def read_courses(db: DbSession) -> list[CourseRead]:
    return list_courses(db)


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
