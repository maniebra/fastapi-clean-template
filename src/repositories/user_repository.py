from datetime import datetime
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.entities.user import Role, User, UserRole
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
            user = await self.db_session.merge(user)
            await self.db_session.commit()
            await self.db_session.refresh(user)
            return user
        except Exception as e:
            print(e)
            await self.db_session.rollback()
            return None

    async def delete_user_by_id(self, user_id: UUID) -> UUID | None:
        try:
            user = await self.get_user_by_id(user_id)
            await self.db_session.delete(user)
            await self.db_session.commit()
            return user_id
        except Exception as e:
            print(e)
            return None

    async def renew_valid_iat_after(self, user_id: UUID) -> datetime | None:
        try:
            user = await self.get_user_by_id(user_id)
            if user is None:
                raise Exception("No such user!")
            new_valid_iat_after = datetime.now()
            user.valid_iat_after = new_valid_iat_after
            _ = await self.update_user(user)
            return new_valid_iat_after
        except Exception as e:
            print(e)
            return None

    async def get_roles(self) -> list[Role]:
        stmt = select(Role).distinct()
        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())

    async def get_role_by_id(self, role_id: int) -> Role | None:
        stmt = select(Role).where(Role.id == role_id)
        return await self.db_session.scalar(stmt)

    async def create_new_role(self, role: Role) -> Role | None:
        try:
            self.db_session.add(role)
            await self.db_session.commit()
            await self.db_session.refresh(role)
            return role
        except Exception as e:
            print(e)
            return None

    async def update_role(self, role: Role) -> Role | None:
        try:
            role = await self.db_session.merge(role)
            await self.db_session.commit()
            await self.db_session.refresh(role)
            return role
        except Exception as e:
            print(e)
            await self.db_session.rollback()
            return None

    async def delete_role(self, role_id: int) -> int | None:
        try:
            role = await self.get_role_by_id(role_id)
            await self.db_session.delete(role)
            await self.db_session.commit()
            return role_id
        except Exception as e:
            print(e)
            return None

    async def add_role_to_user(self, user_id: UUID, role_id: int) -> UserRole | None:
        try:
            user = await self.get_user_by_id(user_id)
            role = await self.get_role_by_id(role_id)
            if user is None or role is None:
                return None

            link = UserRole(user_id=user_id, role_id=role_id)
            self.db_session.add(link)
            await self.db_session.commit()
            await self.db_session.refresh(link)
            return link

        except IntegrityError:
            await self.db_session.rollback()
            res = await self.db_session.execute(
                select(UserRole).where(
                    UserRole.user_id == user_id, UserRole.role_id == role_id
                )
            )
            return res.scalar_one_or_none()

        except SQLAlchemyError:
            await self.db_session.rollback()
            return None

    async def take_role_away_from_user(
        self, user_id: UUID, role_id: int
    ) -> User | None:
        try:
            res = await self.db_session.execute(
                select(UserRole).where(
                    UserRole.user_id == user_id, UserRole.role_id == role_id
                )
            )
            link = res.scalar_one_or_none()
            if link is None:
                return None

            await self.db_session.delete(link)
            await self.db_session.commit()

            user = await self.get_user_by_id(user_id)
            return user

        except SQLAlchemyError:
            await self.db_session.rollback()
            return None
