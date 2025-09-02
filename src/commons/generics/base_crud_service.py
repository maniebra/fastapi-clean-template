from typing import Annotated, TypeVar
from typing import Generic

from fastapi import Depends
from src.commons.generics.base_crud_entity import BaseCrudEntity
from src.commons.generics.base_entity_repository import BaseEntityRepository

T = TypeVar("T", bound=BaseCrudEntity)


class BaseCrudService(Generic[T]):
    def __init__(
        self,
        model: type[T],
        repository: Annotated[
            BaseEntityRepository[T], Depends(BaseEntityRepository[T])
        ],
    ):
        self.repository: BaseEntityRepository[T] = repository
        self.model: type[T] = model

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, entity: T):
        return self.repository.create(entity)

    def update(self, entity: T):
        return self.repository.update(entity)

    def delete(self, id: int):
        return self.repository.delete(id)
