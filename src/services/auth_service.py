from typing import Annotated, final
from uuid import UUID
from fastapi import Depends, HTTPException, status
from src.commons.providers.hash_provider import (
    hash_password_async,
    needs_rehash,
    verify_password_async,
)
from src.entities.user import Role, User
from src.commons.providers.jwt_provider import Claims, create_access_token
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
        password = await hash_password_async(password)
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
            password = await hash_password_async(password)
            user.password = password
        if email is not None:
            user.email = email
        if phone_number is not None:
            user.phone_number = phone_number
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        new_user = await self.repository.update_user(user)
        _ = await self.repository.renew_valid_iat_after(user.id)
        return new_user

    async def change_password(self, user_id: UUID, password: str):
        return await self.update_user(user_id, password=password)

    async def change_email(self, user_id: UUID, email: str):
        return await self.update_user(user_id, email=email)

    async def authenticate_user(self, username: str, password: str) -> str:
        user = await self.get_user_by_username(username)
        invalid_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

        if user is None:
            raise invalid_exc

        is_valid = await verify_password_async(password, user.password)
        if not is_valid:
            raise invalid_exc

        if needs_rehash(user.password):
            new_hash = await hash_password_async(password)
            _ = await self.change_password(user.id, new_hash)

        jwt_map: Claims = {
            "id": str(user.id),
            "username": user.username,
            "roles": [role.name for role in user.roles],
        }
        token: str = create_access_token(jwt_map)
        return token

    async def get_roles(self):
        return await self.repository.get_roles()

    async def get_role_by_id(self, role_id: int):
        return await self.repository.get_role_by_id(role_id)

    async def create_new_role(self, name: str) -> Role | None:
        role = Role(name=name)
        return await self.repository.create_new_role(role)

    async def update_role(self, role: Role):
        return await self.repository.update_role(role)

    async def delete_role(self, role_id: int):
        return await self.repository.delete_role(role_id)

    async def add_role_to_user(self, user_id: UUID, role_id: int):
        user_role = await self.repository.add_role_to_user(user_id, role_id)
        _ = await self.repository.renew_valid_iat_after(user_id)
        return user_role

    async def take_role_away_from_user(self, user_id: UUID, role_id: int):
        user = await self.repository.take_role_away_from_user(user_id, role_id)
        _ = await self.repository.renew_valid_iat_after(user_id)
        return user
