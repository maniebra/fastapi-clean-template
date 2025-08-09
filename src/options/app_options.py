import os

ENTRYPOINT = os.getenv("ENTRYPOINT", "main:app")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
RELOAD = bool(os.getenv("RELOAD", True))
DEBUG = bool(os.getenv("DEBUG", True))

# CORS-RELATED OPTIONS
ALLOWED_HOSTS = list(os.getenv("ALLOWED_HOSTS", "[*]"))
ALLOWED_METHODS = list(os.getenv("ALLOWED_METHODS", "[*]"))
ALLOWED_HEADERS = list(os.getenv("ALLOWED_HEADERS", "[*]"))
ALLOW_CREDENTIALS = bool(os.getenv("ALLOW_CREDENTIALS", True))
