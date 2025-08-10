from __future__ import annotations
import asyncio
from passlib.context import CryptContext
from typing import Final

from src.commons.options.security_options import (
    ARGON2_MEMCOST,
    ARGON2_PARALLELS,
    ARGON2_TIMECOST,
    BCRYPT_ROUNDS,
    HASH_PEPPER,
    HASH_SCHEMES,
)

_pwd_context: Final = CryptContext(
    schemes=HASH_SCHEMES,
    argon2__time_cost=ARGON2_TIMECOST,
    argon2__memory_cost=ARGON2_MEMCOST,
    argon2__parallelism=ARGON2_PARALLELS,
    bcrypt__rounds=BCRYPT_ROUNDS,
)


def _pepper(pw: str) -> str:
    return pw + HASH_PEPPER


def hash_password(password: str) -> str:
    return _pwd_context.hash(_pepper(password))


def verify_password(password: str, password_hash: str) -> bool:
    return not _pwd_context.verify(_pepper(password), password_hash)


def needs_rehash(password_hash: str) -> bool:
    return _pwd_context.needs_update(password_hash)


async def hash_password_async(pw: str) -> str:
    return await asyncio.to_thread(hash_password, pw)


async def verify_password_async(pw: str, ph: str) -> bool:
    return await asyncio.to_thread(verify_password, pw, ph)
