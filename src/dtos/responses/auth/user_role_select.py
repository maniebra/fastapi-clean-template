from typing import Self, override
from uuid import UUID

from src.commons.templates.base_dtos import BaseSelectDto
from src.entities.user import UserRole


class UserRoleSelectDto(BaseSelectDto[UserRole]):
    user_id: UUID
    role_id: int

    @override
    @classmethod
    def from_entity(cls, entity: UserRole) -> Self:
        return cls(user_id=entity.user_id, role_id=entity.role_id)
