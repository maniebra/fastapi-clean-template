from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.options.app_options import ENTRYPOINT, HOST, PORT, RELOAD
from src.routers import auth_router
from src.providers.db_provider import create_db, shutdown_db

app = FastAPI(prefix="/api/v1")


@asynccontextmanager
async def lifespan():
    # Startup
    await create_db()
    yield
    # Shutdown
    await shutdown_db()


app.include_router(auth_router.AuthRouter, prefix="/users")
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(ENTRYPOINT, host=HOST, port=PORT, reload=RELOAD)
