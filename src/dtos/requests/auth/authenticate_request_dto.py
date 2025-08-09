from pydantic import BaseModel


class AuthenticateRequestDto(BaseModel):
    username: str
    password: str
