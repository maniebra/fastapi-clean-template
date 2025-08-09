from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from factbackend.generics.base_model import BaseModel
from factbackend.options.db_options import (
    DATABASE_ECHO_ACTIVATED,
    DATABASE_URL,
    SHOULD_EXPIRE_ON_COMMIT,
)

# Create async engine
main_db_engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=DATABASE_ECHO_ACTIVATED,
)

# Async session maker
AsyncSessionLocal = async_sessionmaker(
    bind=main_db_engine,
    expire_on_commit=SHOULD_EXPIRE_ON_COMMIT,
    class_=AsyncSession,
)


# Dependency for FastAPI
async def get_main_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Create tables
async def create_db():
    async with main_db_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


# Shutdown database
async def shutdown_db():
    await main_db_engine.dispose()
