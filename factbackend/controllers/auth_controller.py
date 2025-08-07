from uuid import UUID
from fastapi.routing import APIRouter

from factbackend.dtos.requests.auth.register_user_request import RegisterUserRequestDto
from factbackend.services import auth_service

AuthController = APIRouter()


@AuthController.get("/")
async def all():
    return await auth_service.get_all_users()


@AuthController.post("/")
async def register_user(request: RegisterUserRequestDto):
    return await auth_service.register_user(
        request.username,
        request.password,
        request.passwordConfirmation,
        request.email,
        request.phone_number,
        request.first_name,
        request.last_name,
    )


@AuthController.delete("/{user_id}")
async def delete_user_by_id(user_id: UUID):
    return await auth_service.delete_user_by_id(user_id)
