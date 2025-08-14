from typing import Annotated
from uuid import UUID
from fastapi import Depends
from fastapi.routing import APIRouter
from src.dtos.requests.auth.authenticate_request_dto import AuthenticateRequestDto
from src.dtos.requests.auth.create_role_dto import CreateRoleDto
from src.dtos.requests.auth.register_user_request import RegisterUserRequestDto
from src.dtos.requests.auth.update_user_request_dto import UpdateUserRequestDto
from src.dtos.responses.auth.__pycache__.user_select_dto import UserSelectDto
from src.dtos.responses.auth.role_select_dto import RoleSelectDto
from src.dtos.responses.auth.user_role_select import UserRoleSelectDto
from src.services.auth_service import AuthService

AuthRouter = APIRouter(tags=["Auth"])


@AuthRouter.get("/")
async def all_users(service: Annotated[AuthService, Depends(AuthService)]):
    users = await service.get_all_users()
    return [UserSelectDto.from_entity(user) for user in users]


@AuthRouter.get("/{user_id}")
async def get_user_by_id(user_id: UUID, service: Annotated[AuthService, Depends()]):
    user = await service.get_user_by_id(user_id)
    if user is None:
        return None
    return UserSelectDto.from_entity(user)


@AuthRouter.get("/username/{username}")
async def get_user_by_username(
    username: str, service: Annotated[AuthService, Depends()]
):
    user = await service.get_user_by_username(username)
    if user is None:
        return None
    return UserSelectDto.from_entity(user)


@AuthRouter.get("/email/{email}")
async def get_user_by_email(email: str, service: Annotated[AuthService, Depends()]):
    user = await service.get_user_by_email(email)
    if user is None:
        return None
    return UserSelectDto.from_entity(user)


@AuthRouter.post("/")
async def register_user(
    request: RegisterUserRequestDto, service: Annotated[AuthService, Depends()]
):
    user = await service.register_user(
        request.username,
        request.password,
        request.passwordConfirmation,
        request.email,
        request.phone_number,
        request.first_name,
        request.last_name,
    )
    if user is None:
        return None
    return UserSelectDto.from_entity(user)


@AuthRouter.put("/{user_id}")
async def update_user(
    user_id: UUID,
    request: UpdateUserRequestDto,
    service: Annotated[AuthService, Depends()],
):
    user = await service.update_user(
        user_id,
        username=request.username,
        password=request.password,
        password_confirmation=request.passwordConfirmation,
        email=request.email,
        phone_number=request.phone_number,
        first_name=request.first_name,
        last_name=request.last_name,
    )
    if user is None:
        return None
    return UserSelectDto.from_entity(user)


@AuthRouter.put("/password/{user_id}")
async def change_password(
    user_id: UUID, password: str, service: Annotated[AuthService, Depends()]
):
    user = await service.change_password(user_id, password)
    if user is None:
        return None
    return UserSelectDto.from_entity(user)


@AuthRouter.put("/email/{user_id}")
async def change_email(
    user_id: UUID, email: str, service: Annotated[AuthService, Depends()]
):
    user = await service.change_email(user_id, email)
    if user is None:
        return None
    return UserSelectDto.from_entity(user)


@AuthRouter.delete("/{user_id}")
async def delete_user_by_id(user_id: UUID, service: Annotated[AuthService, Depends()]):
    user = await service.delete_user_by_id(user_id)
    if user is None:
        return None
    return user_id


@AuthRouter.post("/login")
async def login(
    request: AuthenticateRequestDto, service: Annotated[AuthService, Depends()]
):
    return await service.authenticate_user(request.username, request.password)


# Role-related endpoints
@AuthRouter.delete("/role/{role_id}")
async def delete_role(
    role_id: int, service: Annotated[AuthService, Depends()]
) -> int | None:
    return await service.delete_role(role_id)


@AuthRouter.get("/role/{role_id}")
async def get_role_by_id(
    role_id: int, service: Annotated[AuthService, Depends()]
) -> RoleSelectDto | None:
    role = await service.get_role_by_id(role_id)
    if role is None:
        return None
    return RoleSelectDto.from_entity(role)


@AuthRouter.post("/role")
async def create_new_role(
    new_role: CreateRoleDto, service: Annotated[AuthService, Depends()]
) -> RoleSelectDto | None:
    role = await service.create_new_role(new_role.name)
    if role is None:
        return None
    return RoleSelectDto.from_entity(role)


@AuthRouter.post("/role/{user_id}/{role_id}")
async def add_role_to_user(
    user_id: UUID, role_id: int, service: Annotated[AuthService, Depends()]
) -> UserRoleSelectDto | None:
    user_role = await service.add_role_to_user(user_id, role_id)
    if user_role is None:
        return None
    return UserRoleSelectDto.from_entity(user_role)


@AuthRouter.delete("/role/{user_id}/{role_id}")
async def take_role_away_from_user(
    user_id: UUID, role_id: int, service: Annotated[AuthService, Depends()]
) -> UserSelectDto | None:
    user = await service.take_role_away_from_user(user_id, role_id)
    if user is None:
        return None
    return UserSelectDto.from_entity(user)
