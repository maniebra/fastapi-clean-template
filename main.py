import asyncio
from fastapi import FastAPI

from factbackend.controllers import auth_controller
from factbackend.providers.db_provider import create_db

app = FastAPI(prefix="/api/v1")

@app.on_event("startup")
async def on_startup():
    await create_db()

app.include_router(auth_controller.AuthController, prefix="/users")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
