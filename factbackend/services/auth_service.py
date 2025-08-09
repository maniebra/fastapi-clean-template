from typing import Annotated, final
from uuid import UUID
from fastapi import Depends
from factbackend.entities.user import User
from factbackend.generics.base_main_repository import BaseMainRepository
from factbackend.generics.base_main_service import BaseMainService
from factbackend.repositories.user_repository import UserRepository


@final
class AuthService(BaseMainService):
    def __init__(
        self, repository: Annotated[UserRepository, Depends(UserRepository)]
    ) -> None:
        super().__init__(repository)
        self._repository: BaseMainRepository = repository
        self.repository: UserRepository = self._repository

    async def get_all_users(self):
        return await self.repository.get_all_users()

    async def register_user(
        self,
        username: str,
        password: str,
        passwordConfirmation: str,
        email: str,
        phone_number: str,
        first_name: str,
        last_name: str,
    ):
        if password != passwordConfirmation:
            raise Exception("Passwords do not match")
        user = User(
            username=username,
            password=password,
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
        )
        return await self.repository.create_new_user(user)

    async def delete_user_by_id(self, user_id: UUID):
        return await self.repository.delete_user_by_id(user_id)

    async def get_user_by_id(self, user_id: UUID):
        return await self.repository.get_user_by_id(user_id)
