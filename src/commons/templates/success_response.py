from pydantic import BaseModel


class SuccessResponse[T](BaseModel):
    message: str
    data: T | None
