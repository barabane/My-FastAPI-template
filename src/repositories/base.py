from abc import ABC
from typing import Dict, List, Optional

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.base import BaseModel
from dto.base import BaseDTO


class BaseRepository(ABC):
    def __init__(self, model: BaseModel) -> None:
        self.model: BaseModel = model

    async def get_by_id(self, entity_id, session: AsyncSession) -> BaseModel | None:
        return await session.get(self.model, entity_id)

    async def get_all(
        self, query_params: Optional[Dict[str, str]], session: AsyncSession
    ) -> List[BaseModel]:
        res = await session.execute(select(self.model).filter_by(**query_params))
        return res.scalars().all()

    async def add(self, entity: BaseDTO, session: AsyncSession) -> BaseModel:
        res = await session.execute(
            insert(self.model).values(**entity).returning(self.model)
        )
        return res.scalar_one()

    async def delete_by_id(self, entity_id, session: AsyncSession) -> None:
        await session.execute(delete(self.model).where(self.model.id == entity_id))

    async def update(
        self, new_entity: BaseDTO, entity_id, session: AsyncSession
    ) -> BaseModel:
        res = await session.execute(
            update(self.model)
            .where(self.model.id == entity_id)
            .values(**new_entity)
            .returning(self.model)
        )
        return res.scalar_one()


def get_base_repository() -> BaseRepository:
    return BaseRepository(model=BaseModel)
