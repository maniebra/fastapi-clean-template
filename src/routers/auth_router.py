from typing import Annotated
from uuid import UUID
from fastapi import Depends
from fastapi.routing import APIRouter
from src.dtos.requests.auth.authenticate_request_dto import AuthenticateRequestDto
from src.dtos.requests.auth.register_user_request import RegisterUserRequestDto
from src.dtos.requests.auth.update_user_request_dto import UpdateUserRequestDto
from src.services.auth_service import AuthService

AuthRouter = APIRouter()


@AuthRouter.get("/")
async def all_users(service: Annotated[AuthService, Depends(AuthService)]):
    return await service.get_all_users()


@AuthRouter.get("/{user_id}")
async def get_user_by_id(user_id: UUID, service: Annotated[AuthService, Depends()]):
    return await service.get_user_by_id(user_id)


@AuthRouter.get("/username/{username}")
async def get_user_by_username(
    username: str, service: Annotated[AuthService, Depends()]
):
    return await service.get_user_by_username(username)


@AuthRouter.get("/email/{email}")
async def get_user_by_email(email: str, service: Annotated[AuthService, Depends()]):
    return await service.get_user_by_email(email)


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


@AuthRouter.put("/{user_id}")
async def update_user(
    user_id: UUID,
    request: UpdateUserRequestDto,
    service: Annotated[AuthService, Depends()],
):
    return await service.update_user(
        user_id,
        username=request.username,
        password=request.password,
        password_confirmation=request.passwordConfirmation,
        email=request.email,
        phone_number=request.phone_number,
        first_name=request.first_name,
        last_name=request.last_name,
    )


@AuthRouter.put("/password/{user_id}")
async def change_password(
    user_id: UUID, password: str, service: Annotated[AuthService, Depends()]
):
    return await service.change_password(user_id, password)


@AuthRouter.put("/email/{user_id}")
async def change_email(
    user_id: UUID, email: str, service: Annotated[AuthService, Depends()]
):
    return await service.change_email(user_id, email)


@AuthRouter.delete("/{user_id}")
async def delete_user_by_id(user_id: UUID, service: Annotated[AuthService, Depends()]):
    return await service.delete_user_by_id(user_id)


@AuthRouter.post("/login")
async def login(
    request: AuthenticateRequestDto, service: Annotated[AuthService, Depends()]
):
    return await service.authenticate_user(request.username, request.password)
