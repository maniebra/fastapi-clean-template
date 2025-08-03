from typing import Annotated
from fastapi import Depends
from dmpbackend.entities.user import User
from dmpbackend.repositories.user_repository import UserRepository

class AuthService:
    def __init__(self, repository: UserRepository = Depends()) -> None:
        self.repository : UserRepository = repository

    async def get_all_users(self):
        return await self.repository.get_all_users()

    async def get_user_by_id(self, re)

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
