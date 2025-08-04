from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from factbackend.entities.user import User
from factbackend.providers.db_provider import get_main_db
from fastapi import Depends

class UserRepository:
    def __init__(self, main_db_session: AsyncSession = Depends(get_main_db)) -> None:
        self.db_session: AsyncSession = main_db_session

    async def get_all_users(self):
        stmt = select(User)
        result = await self.db_session.scalar(stmt)
        return result

    async def get_user_by_id(self, user_id: UUID):
        stmt = select(User).where(User.id == user_id)
        result = await self.db_session.scalar(stmt)
        return result

    async def create_new_user(self, user: User) -> User | None:
        try:
            self.db_session.add(user)
            await self.db_session.commit()
            return user
        except Exception:
            return None

    async def delete_user_by_id(self, user_id: UUID) -> UUID | None:
        try:
            user = await self.get_user_by_id(user_id)
            await self.db_session.delete(user)
            await self.db_session.commit()
            return user_id
        except Exception:
            return None
