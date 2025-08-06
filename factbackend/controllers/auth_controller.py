from fastapi.routing import APIRouter

from factbackend.services import auth_service

AuthController = APIRouter()

@AuthController.get("/")
async def all():
    return await auth_service.get_all_users()

@AuthController.post("/")
async def register_user(
    username: str,
    password: str, 
    passwordConfirmation: str,
    email: str,
    phone_number: str,
    first_name: str,
    last_name: str
    ):
    return await auth_service.register_user(username, password, passwordConfirmation, email, phone_number, first_name, last_name)

@AuthController.delete("/{user_id}")
async def delete_user_by_id(user_id: UUID):
    return await auth_service.delete_user_by_id(user_id)
