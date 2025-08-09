from contextlib import asynccontextmanager
from fastapi import FastAPI

from factbackend.routers import auth_router
from factbackend.providers.db_provider import create_db

app = FastAPI(prefix="/api/v1")

@asynccontextmanager
async def lifespan():
    # Startup
    await create_db()
    yield
    # Shutdown
    # TODO: A CLOSE CONNECTION SHOULD GO HERE!

app.include_router(auth_router.AuthRouter, prefix="/users")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
