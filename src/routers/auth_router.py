from typing import Annotated
from uuid import UUID
from fastapi import Depends
from fastapi.routing import APIRouter
from src.dtos.requests.auth.register_user_request import RegisterUserRequestDto
from src.services.auth_service import AuthService

AuthRouter = APIRouter()


@AuthRouter.get("/")
async def all(service: Annotated[AuthService, Depends(AuthService)]):
    return await service.get_all_users()


@AuthRouter.post("/")
async def register_user(
    request: RegisterUserRequestDto, service: Annotated[AuthService, Depends()]
):
    return await service.register_user(
        request.username,
        request.password,
        request.passwordConfirmation,
        request.email,
        request.phone_number,
        request.first_name,
        request.last_name,
    )


@AuthRouter.delete("/{user_id}")
async def delete_user_by_id(user_id: UUID, service: Annotated[AuthService, Depends()]):
    return await service.delete_user_by_id(user_id)
