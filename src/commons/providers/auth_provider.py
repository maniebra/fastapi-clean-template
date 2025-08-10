from fastapi import Depends, HTTPException, Request, status
from typing import Annotated, cast
from src.middlewares.bearer_auth_middleware import AuthContext


def get_auth_optional(request: Request) -> AuthContext | None:
    return cast(AuthContext | None, getattr(request.state, "auth", None))


def require_auth(
    auth: Annotated[AuthContext | None, Depends(get_auth_optional)],
) -> AuthContext:
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth


def has_role(*required_roles: str):
    required = {r.lower() for r in required_roles}

    def dep(auth: Annotated[AuthContext, Depends(require_auth)]) -> AuthContext:
        if not required.issubset({r.lower() for r in auth.roles}):
            raise HTTPException(status_code=403, detail="Insufficient role")
        return auth

    return dep


def not_banned(auth: Annotated[AuthContext, Depends(require_auth)]) -> AuthContext:
    if auth.is_banned:
        raise HTTPException(status_code=403, detail="User is banned")
    return auth
