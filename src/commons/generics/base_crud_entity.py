from sqlalchemy.orm import Mapped, mapped_column
from src.commons.generics.base_entity import BaseEntity


class BaseCrudEntity(BaseEntity):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
