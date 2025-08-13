from src.commons.providers.hash_provider import (
    verify_password_async,
    hash_password_async,
)
import pytest


@pytest.mark.asyncio
async def test_password_verification_valid_and_invalid():
    hashed = await hash_password_async("Mojave")

    assert await verify_password_async("Mojave", hashed) is True
    assert await verify_password_async("Skewrite", hashed) is False


@pytest.mark.asyncio
async def test_password_verification_malformed_hash_is_false():
    try:
        ok = await verify_password_async("Mawe1234", "8ua8f9hsd")
    except Exception:
        ok = False
    assert ok is False
