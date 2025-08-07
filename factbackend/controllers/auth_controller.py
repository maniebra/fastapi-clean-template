from uuid import UUID
from fastapi import Depends
from fastapi.routing import APIRouter
from factbackend.dtos.requests.auth.register_user_request import RegisterUserRequestDto
from factbackend.services.auth_service import AuthService

AuthController = APIRouter()


@AuthController.get("/")
async def all(service : AuthService = Depends(AuthService)):
    return await service.get_all_users()

@AuthController.post("/")
async def register_user(request: RegisterUserRequestDto, service : AuthService = Depends()):
    return await service.register_user(
        request.username,
        request.password,
        request.passwordConfirmation,
        request.email,
        request.phone_number,
        request.first_name,
        request.last_name,
    )


@AuthController.delete("/{user_id}")
async def delete_user_by_id(user_id: UUID, service : AuthService = Depends()):
    return await service.delete_user_by_id(user_id)
