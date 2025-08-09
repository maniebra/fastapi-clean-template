from typing import Annotated
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.providers.db_provider import get_main_db


class BaseMainRepository:
    def __init__(
        self, main_db_session: Annotated[AsyncSession, Depends(get_main_db)]
    ) -> None:
        self.db_session: AsyncSession = main_db_session
