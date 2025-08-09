from pydantic import BaseModel


class UpdateUserRequestDto(BaseModel):
    username: str | None = None
    password: str | None = None
    passwordConfirmation: str | None = None
    email: str | None = None
    phone_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None
