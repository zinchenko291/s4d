import os

from dependency_injector.wiring import inject, Provide

from src.container import Container
from src.infrastructure.services import RabbitRepository

from src import shared_vars, Config, BaseRepository


@inject
async def runner(rabbit_repository: RabbitRepository = Provide[Container.rabbit_repository], config: Config = Provide[Container.config], base_repository: BaseRepository = Provide[Container.base_repository]):
    shared_vars.base_repository = base_repository
    await rabbit_repository.connect()

