from typing import Annotated, final
from uuid import UUID
from fastapi import Depends
from src.entities.user import User
from src.commons.providers.jwt_provider import create_access_token
from src.repositories.user_repository import UserRepository


@final
class AuthService:
    def __init__(
        self, user_repository: Annotated[UserRepository, Depends(UserRepository)]
    ) -> None:
        self.repository: UserRepository = user_repository

    async def get_all_users(self):
        return await self.repository.get_all_users()

    async def register_user(
        self,
        username: str,
        password: str,
        password_confirmation: str,
        email: str,
        phone_number: str,
        first_name: str,
        last_name: str,
    ):
        if password != password_confirmation:
            raise Exception("Passwords do not match")
        # TODO: Hash the password!
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

    async def get_user_by_username(self, username: str):
        return await self.repository.get_user_by_username(username)

    async def get_user_by_email(self, email: str):
        return await self.repository.get_user_by_email(email)

    async def update_user(
        self,
        user_id: UUID,
        username: str | None = None,
        password: str | None = None,
        password_confirmation: str | None = None,
        email: str | None = None,
        phone_number: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ):
        user = await self.get_user_by_id(user_id)
        if user is None:
            raise Exception("User not found")
        if username is not None:
            user.username = username
        if password is not None:
            if password != password_confirmation:
                raise Exception("Passwords do not match")
            user.password = password
        if email is not None:
            user.email = email
        if phone_number is not None:
            user.phone_number = phone_number
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        return await self.repository.update_user(user)

    async def change_password(self, user_id: UUID, password: str):
        return await self.update_user(user_id, password=password)

    async def change_email(self, user_id: UUID, email: str):
        return await self.update_user(user_id, email=email)

    async def authenticate_user(self, username: str, password: str):
        user = await self.get_user_by_username(username)
        if user is None:
            raise Exception("User not found")
        if user.password != password:
            raise Exception("Invalid password")
        jwt_map = {"id": str(user.id), "username": user.username}
        token: str = create_access_token(jwt_map)
        return token
