import os

ENTRYPOINT = os.getenv("ENTRYPOINT", "main:app")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = os.getenv("PORT", 8000)
RELOAD = os.getenv("RELOAD", True)
DEBUG = os.getenv("DEBUG", True)
