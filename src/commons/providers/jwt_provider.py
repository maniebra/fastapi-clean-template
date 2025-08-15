from __future__ import annotations

from collections.abc import Mapping
from typing import Callable, TypeAlias, TypeGuard, cast

from datetime import datetime, timedelta, timezone

import jwt
from jwt import ExpiredSignatureError, PyJWTError

from src.commons.options.jwt_options import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)

JSONPrimitive: TypeAlias = str | int | float | bool
JSONScalar: TypeAlias = JSONPrimitive | list[JSONPrimitive]
Claims: TypeAlias = dict[str, JSONScalar]


def _is_json_primitive(v: object) -> TypeGuard[JSONPrimitive]:
    return isinstance(v, (str, int, float, bool))


def _is_json_scalar(v: object) -> TypeGuard[JSONScalar]:
    if _is_json_primitive(v):
        return True
    if isinstance(v, list):
        elems = cast(list[object], v)
        return all(_is_json_primitive(x) for x in elems)
    return False


def _is_claims(obj: object) -> TypeGuard[Claims]:
    if not isinstance(obj, dict):
        return False
    items = cast(dict[object, object], obj).items()
    for k, v in items:
        if not isinstance(k, str):
            return False
        if not _is_json_scalar(v):
            return False
    return True


_encode: Callable[..., str] = cast(Callable[..., str], jwt.encode)
_decode: Callable[..., dict[str, object]] = cast(
    Callable[..., dict[str, object]], jwt.decode
)


def create_access_token(
    data: Mapping[str, JSONScalar],
    expires_delta: timedelta | None = None,
) -> str:
    # Make a copy we can mutate safely
    to_encode: Claims = dict(data)

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    # Store exp as an int UNIX timestamp (fits JSONPrimitive)
    to_encode["exp"] = int(expire.timestamp())
    to_encode["iat"] = int(datetime.now().timestamp())

    return _encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> Claims | None:
    try:
        decoded = _decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        return None
    except PyJWTError:
        return None

    if _is_claims(decoded):
        return decoded
    return None
