from uuid import UUID
from sqlalchemy import select
from src.entities.user import User
from src.commons.generics.base_main_repository import BaseMainRepository


class UserRepository(BaseMainRepository):
    async def get_all_users(self):
        stmt = select(User).distinct()
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get_user_by_username(self, username: str):
        stmt = select(User).where(User.username == username)
        result = await self.db_session.scalar(stmt)
        return result

    async def get_user_by_email(self, email: str):
        stmt = select(User).where(User.email == email)
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
            await self.db_session.refresh(user)
            return user
        except Exception as e:
            print(e)
            await self.db_session.rollback()
            return None

    async def update_user(self, user: User) -> User | None:
        try:
            self.db_session.add(user)
            await self.db_session.commit()
            await self.db_session.refresh(user)
            return user
        except Exception:
            await self.db_session.rollback()
            return None

    async def delete_user_by_id(self, user_id: UUID) -> UUID | None:
        try:
            user = await self.get_user_by_id(user_id)
            await self.db_session.delete(user)
            await self.db_session.commit()
            return user_id
        except Exception:
            return None
