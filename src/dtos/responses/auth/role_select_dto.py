from typing import Self, override
from src.commons.templates.base_dtos import BaseSelectDto
from src.entities.user import Role


class RoleSelectDto(BaseSelectDto[Role]):
    id: int
    name: str

    @classmethod
    @override
    def from_entity(cls, entity: Role) -> Self:
        return cls(id=entity.id, name=entity.name)
