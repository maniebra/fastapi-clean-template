from typing import Self
from pydantic import BaseModel


class BaseSelectDto[T](BaseModel):
    @classmethod
    def from_entity(cls, entity: T) -> Self:
        raise NotImplementedError(f"You must convert {entity} to proper select DTO!")


class BaseRequestDto[T](BaseModel):
    def to_entity(self) -> T:
        raise NotImplementedError("You must convert the DTO to a proper entity!")
