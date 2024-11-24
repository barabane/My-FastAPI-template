from abc import ABC
from typing import List, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.database.models.base import BaseModel
from src.dto.base import BaseDTO
from src.exceptions import NotFoundException
from src.repositories.base import BaseRepository, get_base_repository
from src.schemas.base import BaseSChemas, get_base_schemas


class BaseService(ABC):
    def __init__(self, repository: BaseRepository, schemas: BaseSChemas) -> None:
        self.repository: BaseRepository = repository
        self.schemas: BaseSChemas = schemas

    async def get_by_id(
        self, entity_id, session: AsyncSession = Depends(get_async_session)
    ):
        res: BaseModel | None = await self.repository.get_by_id(
            entity_id=entity_id, session=session
        )
        if not res:
            raise NotFoundException()

        return self.schemas.get_scheme(**res.__dict__)

    async def get_all(
        self,
        session: AsyncSession = Depends(get_async_session),
    ):
        res: Optional[List[BaseModel]] = await self.repository.get_all(session=session)
        return [self.schemas.get_scheme(**model.__dict__) for model in res]

    async def add(
        self, entity: BaseDTO, session: AsyncSession = Depends(get_async_session)
    ):
        res: BaseModel = await self.repository.add(entity=entity, session=session)

        return self.schemas.get_scheme(**res.__dict__)

    async def delete_by_id(
        self, entity_id, session: AsyncSession = Depends(get_async_session)
    ) -> None:
        await self.get_by_id(entity_id=entity_id, session=session)

        return await self.repository.delete_by_id(entity_id=entity_id, session=session)

    async def update(
        self,
        new_entity: BaseDTO,
        entity_id,
        session: AsyncSession = Depends(get_async_session),
    ) -> BaseModel:
        await self.get_by_id(entity_id=entity_id, session=session)

        res: BaseModel = await self.repository.update(
            new_entity=new_entity, entity_id=entity_id, session=session
        )
        return self.schemas.get_scheme(**res.__dict__)


def get_base_service() -> BaseService:
    return BaseService(repository=get_base_repository(), schemas=get_base_schemas())
