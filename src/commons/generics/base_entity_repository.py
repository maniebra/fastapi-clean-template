from typing import Annotated, Generic, TypeVar
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.sql import Select

from src.commons.generics.base_crud_entity import BaseCrudEntity
from src.commons.generics.base_main_repository import BaseMainRepository
from src.commons.providers.db_provider import get_main_db

T = TypeVar("T", bound=BaseCrudEntity)


class BaseEntityRepository(BaseMainRepository, Generic[T]):
    def __init__(
        self,
        model: type[T],
        main_db_session: Annotated[AsyncSession, Depends(get_main_db)],
    ) -> None:
        super().__init__(main_db_session)
        self.model: type[T] = model

    async def get_all(self) -> list[T]:
        stmt: Select[tuple[T]] = select(self.model)
        result: Result[tuple[T]] = await self.db_session.execute(stmt)
        scalars: ScalarResult[T] = result.scalars()
        items: list[T] = list(scalars.all())
        return items

    async def get_by_id(self, id: int) -> T | None:
        stmt: Select[tuple[T]] = select(self.model).where(self.model.id == id)
        result: Result[tuple[T]] = await self.db_session.execute(stmt)
        entity: T | None = result.scalar_one_or_none()
        return entity

    async def create(self, entity: T) -> T | None:
        try:
            self.db_session.add(entity)
            await self.db_session.commit()
            await self.db_session.refresh(entity)
            return entity
        except Exception as e:
            print(e)
            await self.db_session.rollback()
            return None

    async def update(self, entity: T) -> T | None:
        try:
            entity = await self.db_session.merge(entity)
            await self.db_session.commit()
            await self.db_session.refresh(entity)
            return entity
        except Exception as e:
            print(e)
            await self.db_session.rollback()
            return None

    async def delete(self, id: int) -> int | None:
        try:
            entity = await self.get_by_id(id)
            await self.db_session.delete(entity)
            await self.db_session.commit()
            return id
        except Exception as e:
            print(e)
            return None
