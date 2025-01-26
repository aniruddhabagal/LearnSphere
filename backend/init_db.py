# init_db.py
import asyncio
from database import engine
from models import Base

async def init_models():
    async with engine.begin() as conn:
        # Drop all tables (optional, for development)
        # await conn.run_sync(Base.metadata.drop_all)
        
        # Create tables
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())
    print("Database tables created successfully.")
