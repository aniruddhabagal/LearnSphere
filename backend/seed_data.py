# seed_data.py
import asyncio
from database import get_db
from models import Course, Material

async def seed_data():
    async for session in get_db():
        course = Course(name="Biology 101", description="Introduction to Biology")
        session.add(course)
        await session.flush()  # To get the course ID

        material1 = Material(
            course_id=course.id,
            title="Photosynthesis",
            content="Photosynthesis is the process by which green plants use sunlight to synthesize foods..."
        )
        material2 = Material(
            course_id=course.id,
            title="Cell Structure",
            content="All organisms are composed of cells..."
        )
        session.add_all([material1, material2])
        await session.commit()
        print("Sample data inserted successfully.")

if __name__ == "__main__":
    asyncio.run(seed_data())
