from typing import Annotated
from uuid import UUID
from fastapi import Depends
from factbackend.entities.user import User
from factbackend.repositories.user_repository import UserRepository

class AuthService:
    def __init__(self, repository: UserRepository = Depends()) -> None:
        self.repository : UserRepository = repository

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
        last_name: str
        ):
        if password != passwordConfirmation:
            raise Exception("WHAT THE FUCK!")
        user = User(
                username = username,
                password = password, 
                email = email,
                phone_number = phone_number,
                first_name = first_name,
                last_name = last_name
                )
        return await self.repository.create_new_user(user)

    async def delete_user_by_id(self, user_id: UUID):
        return await self.repository.delete_user_by_id(user_id)

    async def get_user_by_id(self, user_id: UUID):
        return await self.repository.get_user_by_id(user_id)
