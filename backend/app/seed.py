from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.course import Course


COURSES = [
    {
        "title": "Foundations of LearningOS",
        "slug": "foundations-of-learningos",
        "description": "Build a durable learning workflow using goals, feedback loops, and structured reflection.",
        "level": "Beginner",
        "duration_minutes": 90,
    },
    {
        "title": "Applied Systems Thinking",
        "slug": "applied-systems-thinking",
        "description": "Map complex problems, identify leverage points, and turn ambiguity into executable plans.",
        "level": "Intermediate",
        "duration_minutes": 150,
    },
    {
        "title": "AI-Assisted Research Practice",
        "slug": "ai-assisted-research-practice",
        "description": "Use AI tools to gather, challenge, synthesize, and document research with traceable judgment.",
        "level": "Advanced",
        "duration_minutes": 180,
    },
]


def seed_courses() -> None:
    with SessionLocal() as db:
        existing_slugs = set(db.scalars(select(Course.slug)).all())
        for item in COURSES:
            if item["slug"] not in existing_slugs:
                db.add(Course(**item))
        db.commit()


if __name__ == "__main__":
    seed_courses()
