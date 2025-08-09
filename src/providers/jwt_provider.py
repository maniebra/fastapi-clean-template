from __future__ import annotations
from collections.abc import Mapping
from typing import Callable, TypeAlias, cast

from datetime import datetime, timedelta, timezone

import jwt
from jwt import ExpiredSignatureError, PyJWTError

from src.options.jwt_options import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

JSONScalar: TypeAlias = str | int | float | bool
Claims: TypeAlias = dict[str, object]

_encode: Callable[..., str] = cast(Callable[..., str], jwt.encode)
_decode: Callable[..., dict[str, object]] = cast(
    Callable[..., dict[str, object]], jwt.decode
)


def create_access_token(
    data: Mapping[str, JSONScalar],
    expires_delta: timedelta | None = None,
) -> str:
    to_encode: Claims = dict(data)
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode["exp"] = int(expire.timestamp())  # UTC, integer exp
    return _encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> Claims | None:
    try:
        decoded = _decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except ExpiredSignatureError:
        return None
    except PyJWTError:
        return None
