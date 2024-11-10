from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.base import BaseModel
from src.dto.base import BaseDTO
from src.repositories.base import BaseRepository, get_base_repository
from src.schemas.base import BaseSChemas, get_base_schemas


class BaseService(ABC):
    def __init__(self, repository: BaseRepository, schemas: BaseSChemas) -> None:
        self.repository: BaseRepository = repository
        self.schemas: BaseSChemas = schemas

    async def get_by_id(self, entity_id, session: AsyncSession):
        res: BaseModel | None = await self.repository.get_by_id(
            entity_id=entity_id, session=session
        )
        return self.schemas.get_scheme(**res.__dict__)

    async def add(self, entity: BaseDTO, session: AsyncSession):
        res: BaseModel = await self.repository.add(entity=entity, session=session)
        return self.schemas.get_scheme(**res.__dict__)

    async def delete_by_id(self, entity_id, session: AsyncSession) -> None:
        return self.repository.delete_by_id(entity_id=entity_id, session=session)

    async def update(
        self, new_entity: BaseDTO, entity_id, session: AsyncSession
    ) -> BaseModel:
        res = await self.repository.update(
            new_entity=new_entity, entity_id=entity_id, session=session
        )
        return self.schemas.get_scheme(**res.__dict__)


def get_base_service() -> BaseService:
    return BaseService(repository=get_base_repository(), schemas=get_base_schemas())
