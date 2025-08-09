import os

ENTRYPOINT = os.getenv("ENTRYPOINT", "main:app")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
RELOAD = bool(os.getenv("RELOAD", True))
DEBUG = bool(os.getenv("DEBUG", True))
