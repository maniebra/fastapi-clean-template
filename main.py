from contextlib import asynccontextmanager
from fastapi import FastAPI

from factbackend.options.app_options import ENTRYPOINT, HOST, PORT, RELOAD
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

    uvicorn.run(ENTRYPOINT, host=HOST, port=PORT, reload=RELOAD)
