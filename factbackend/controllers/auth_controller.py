from fastapi.routing import APIRouter

from factbackend.services import auth_service

AuthController = APIRouter()

@AuthController.get("/")
async def all():
    return await auth_service.get_all_users()
