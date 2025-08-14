from typing import override
from src.commons.templates.base_dtos import BaseRequestDto
from src.entities.user import Role


class CreateRoleDto(BaseRequestDto[Role]):
    name: str

    @override
    def to_entity(self) -> Role:
        return Role(name=self.name)
