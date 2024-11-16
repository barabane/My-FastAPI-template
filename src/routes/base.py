import abc
from typing import List, Optional

from fastapi.routing import APIRoute, APIRouter

from src.services.base import BaseService


class BaseRouter(APIRouter, abc.ABC):
    def __init__(self, service: BaseService, prefix: str, tags: list[str]) -> None:
        self.service: BaseService = service
        self.tags: List[str] = tags

        super().__init__(prefix=prefix, tags=self.tags)

        self.add_api_route(
            api_route=APIRoute(
                path=prefix + '/all',
                tags=self.tags,
                endpoint=self.service.get_all,
                methods=['GET'],
                response_model=List[Optional[self.service.schemas.get_scheme]],
            )
        )

        self.add_api_route(
            api_route=APIRoute(
                path=prefix,
                tags=self.tags,
                endpoint=self.service.get_by_id,
                methods=['GET'],
                response_model=Optional[self.service.schemas.get_scheme],
            )
        )

        self.add_api_route(
            api_route=APIRoute(
                path=prefix,
                tags=self.tags,
                endpoint=self.service.delete_by_id,
                methods=['DELETE'],
                response_model=None,
            )
        )

        self.add_api_route(
            api_route=APIRoute(
                path=prefix,
                tags=self.tags,
                endpoint=self.service.update,
                methods=['PATCH'],
                response_model=Optional[self.service.schemas.get_scheme],
            )
        )

    def add_api_route(self, api_route: APIRoute):
        self.routes.append(api_route)

    def delete_route(self, api_route: APIRoute):
        self.routes.remove(api_route)
