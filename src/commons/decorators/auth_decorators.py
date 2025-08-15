from collections.abc import Iterable
from typing import Annotated, TypeGuard, cast

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_decorators import depends  # pyright: ignore[reportMissingTypeStubs]

from src.commons.providers.jwt_provider import Claims, verify_token


def _is_str_list(v: object) -> TypeGuard[list[str]]:
    if not isinstance(v, list):
        return False
    objs = cast(list[object], v)
    return all(isinstance(x, str) for x in objs)


def _get_str_list_claim(claims: Claims, key: str) -> list[str] | None:
    v = claims.get(key)
    if _is_str_list(v):
        return v
    return None


def _check_logged_in(token: str | None) -> bool:
    if token is None:
        return False
    return verify_token(token) is not None


def _check_has_roles(token: str | None, roles: Iterable[str]) -> bool:
    if token is None:
        return False
    claims = verify_token(token)
    if claims is None:
        return False
    claim_roles = _get_str_list_claim(claims, "roles")
    if claim_roles is None:
        return False
    return all(role in claim_roles for role in roles)


bearer = HTTPBearer(auto_error=False)


@depends
def is_logged_in(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)] = None,
) -> None:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )

    token = credentials.credentials.strip()
    if not token or not _check_logged_in(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )


def has_roles(*required_roles: str):
    @depends
    def _enforce(
        credentials: Annotated[
            HTTPAuthorizationCredentials | None, Depends(bearer)
        ] = None,
    ) -> None:
        if credentials is None or credentials.scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid Authorization header",
            )

        token = credentials.credentials.strip()
        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Missing bearer token"
            )

        if not _check_has_roles(token, required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: missing required roles",
            )

    return _enforce
