from pydantic import BaseModel


class FailureResponse[T](BaseModel):
    message: str
    data: T | None
    stack_trace: str | None
