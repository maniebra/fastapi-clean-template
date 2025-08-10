import os
from typing import Final

HASH_SCHEMES: Final[list[str]] = os.getenv(
    "PASSWORD_HASHING_SCHEMES", "argon2,bcrypt"
).split(",")
HASH_PEPPER: Final[str] = os.getenv("PASSWORD_PEPPER", "")

ARGON2_TIMECOST: Final[int] = int(os.getenv("ARGON2_TIMECOST", 3))
ARGON2_MEMCOST: Final[int] = int(os.getenv("ARGON2_MEMCOST", 65536))
ARGON2_PARALLELS: Final[int] = int(os.getenv("ARGON2_PARALLELS", 2))
BCRYPT_ROUNDS: Final[int] = int(os.getenv("BCRYPT_ROUNDS", 12))
