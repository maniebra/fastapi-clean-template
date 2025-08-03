from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

from dmpbackend.generics.base_model import BaseModel

# Create async engine
DATABASE_URL = "sqlite+aiosqlite:///./your_db_file.db"
main_db_engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

# Async session maker
AsyncSessionLocal = async_sessionmaker(
    bind=main_db_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Dependency for FastAPI
async def get_main_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# Create tables
async def create_db():
    async with main_db_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

