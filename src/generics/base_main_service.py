from typing import Annotated
from fastapi import Depends
from src.generics.base_main_repository import BaseMainRepository


class BaseMainService:
    def __init__(self, repository: Annotated[BaseMainRepository, Depends()]) -> None:
        self._repository: BaseMainRepository = repository
