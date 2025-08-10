from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

from src.commons.options.app_options import (
    ALLOW_CREDENTIALS,
    ALLOWED_HEADERS,
    ALLOWED_HOSTS,
    ALLOWED_METHODS,
    ENTRYPOINT,
    HOST,
    PORT,
    RELOAD,
)
from src.commons.providers.openapi_provider import build_openapi
from src.middlewares.bearer_auth_middleware import BearerAuthMiddleware
from src.routers import auth_router
from src.commons.providers.db_provider import create_db, shutdown_db

app = FastAPI(prefix="/api/v1")

bearer = HTTPBearer(auto_error=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
)

app.add_middleware(
    BearerAuthMiddleware,
    attach_only=True,
    public_paths={"/", "/health", "/docs", "/redoc", "/openapi.json"},
)

app.openapi = lambda: build_openapi(app)


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
