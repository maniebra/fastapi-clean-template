from __future__ import annotations

from dataclasses import dataclass
from typing import Final, cast
from collections.abc import Iterable

from starlette.types import ASGIApp, Scope, Receive, Send
from starlette.datastructures import Headers
from starlette.responses import JSONResponse

from src.commons.providers.jwt_provider import verify_token, Claims


@dataclass(slots=True, frozen=True)
class AuthContext:
    subject: str | None
    roles: tuple[str, ...]
    is_banned: bool
    claims: Claims


def _parse_roles(value: object) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        seq: Iterable[object] = value
        return tuple(str(item) for item in seq)
    return ()


def _build_context(claims: Claims) -> AuthContext:
    sub = cast(str | None, claims.get("sub")) if "sub" in claims else None
    roles = _parse_roles(claims.get("roles"))
    raw_banned = claims.get("is_banned")
    is_banned = raw_banned is True  # accept only a real boolean True
    return AuthContext(subject=sub, roles=roles, is_banned=is_banned, claims=claims)


class BearerAuthMiddleware:
    """
    - attach_only=True: never blocks; just sets request.state.auth (or None)
    - attach_only=False: blocks 401 on missing/invalid token except for public paths
    """

    app: ASGIApp
    public_paths: set[str]
    attach_only: bool

    _default_public: Final[set[str]] = {
        "/docs",
        "/redoc",
        "/openapi.json",
        "/health",
        "/",
    }

    def __init__(
        self,
        app: ASGIApp,
        *,
        public_paths: Iterable[str] | None = None,
        attach_only: bool = True,
    ) -> None:
        self.app = app
        self.public_paths = set(public_paths or self._default_public)
        self.attach_only = attach_only

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        path = cast(str, scope.get("path", "/"))
        headers = Headers(scope=scope)

        state_obj = scope.get("state")
        if isinstance(state_obj, dict):
            state = cast(dict[str, object], state_obj)
        else:
            state = {}
            scope["state"] = state

        def unauthorized() -> JSONResponse:
            return JSONResponse(
                {"detail": "Not authenticated"},
                status_code=401,
                headers={"WWW-Authenticate": "Bearer"},
            )

        auth_header = headers.get("authorization")
        bearer_token: str | None = None
        if auth_header and auth_header.lower().startswith("bearer "):
            bearer_token = auth_header[7:].strip()

        if path in self.public_paths:
            if bearer_token:
                claims = verify_token(bearer_token)
                state["auth"] = _build_context(claims) if claims else None
            else:
                state["auth"] = None
            await self.app(scope, receive, send)
            return

        if not bearer_token:
            state["auth"] = None
            if self.attach_only:
                await self.app(scope, receive, send)
            else:
                await unauthorized()(scope, receive, send)
            return

        claims = verify_token(bearer_token)
        if not claims:
            state["auth"] = None
            if self.attach_only:
                await self.app(scope, receive, send)
            else:
                await unauthorized()(scope, receive, send)
            return

        state["auth"] = _build_context(claims)
        await self.app(scope, receive, send)
