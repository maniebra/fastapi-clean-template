from pydantic import BaseModel


class RegisterUserRequestDto(BaseModel):
    username: str
    password: str
    passwordConfirmation: str
    email: str
    phone_number: str
    first_name: str
    last_name: str
