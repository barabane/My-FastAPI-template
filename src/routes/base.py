import abc
from typing import Callable, Dict, List, Optional

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.base import BaseGetScheme
from src.database.database import get_async_session
from src.services.base import BaseService


class BaseRouter(abc.ABC):
    def __init__(self, service: BaseService, prefix: str, tags: list[str]) -> None:
        self.service: BaseService = service
        self.tags: List[str] = tags
        self._router = APIRouter()

        self.__define_base_methods()

        super().__init__(prefix=prefix, tags=self.tags)

    def __define_base_methods(self):
        get_scheme: BaseGetScheme = self.service.schemas.get_scheme

        async def get_entity_by_id(
            self, entity_id, session: AsyncSession = Depends(get_async_session)
        ) -> get_scheme:  # type: ignore
            return await self.service.get_by_id(entity_id=entity_id, session=session)

        async def get_all_entities(
            self,
            query_params: Optional[Dict[str, str]] = {},
            session: AsyncSession = Depends(get_async_session),
        ) -> List[get_scheme]:  # type: ignore
            return await self.service.get_all(
                query_params=query_params, session=session
            )

        async def delete_entity_by_id(
            self, entity_id, session: AsyncSession = Depends(get_async_session)
        ) -> None:
            return await self.service.delete_by_id(entity_id=entity_id, session=session)

        async def update_entity_by_id(
            self,
            new_entity,
            entity_id,
            session: AsyncSession = Depends(get_async_session),
        ) -> get_scheme:  # type: ignore
            return await self.service.update(
                new_entity=new_entity, entity_id=entity_id, session=session
            )

        async def add_entity(
            self, entity, session: AsyncSession = Depends(get_async_session)
        ) -> get_scheme:  # type: ignore
            return await self.service.add(entity=entity, session=session)

        self.add_api_route(path='/all', endpoint=get_all_entities)
        self.add_api_route(path='/{entity_id}', endpoint=get_entity_by_id)
        self.add_api_route(path='/{entity_id}', endpoint=delete_entity_by_id)
        self.add_api_route(path='/{entity_id}', endpoint=update_entity_by_id)
        self.add_api_route(path='', endpoint=add_entity)

    def add_api_route(
        self,
        path: str,
        endpoint: Callable,
        methods: List[str] = ['GET'],
        tags: List[str] = None,
        **kwargs,
    ):
        self._router.add_api_route(
            path=self.prefix + path,
            tags=self.tags if tags is None else tags,
            endpoint=endpoint,
            methods=methods**kwargs,
        )

    def delete_api_route(self, path: str, method: str = 'GET'):
        for route in self._router.routes:
            if route.path == self.prefix + path and method in route.methods:
                self._router.routes.remove(route)

    def rewrite_api_route(
        self, old_path: str, new_path: str, endpoint: Callable, method: str = 'GET'
    ):
        self.delete_api_route(old_path, method=method)
        self.add_api_route(path=new_path, endpoint=endpoint, methods=[method])
