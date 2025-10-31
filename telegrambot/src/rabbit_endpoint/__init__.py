from dependency_injector.wiring import inject, Provide

from src.container import Container
from src.infrastructure.services import RabbitRepository

from src.rabbit_endpoint import endpoints

@inject
async def register_routes(rabbit_repository: RabbitRepository = Provide[Container.rabbit_repository]):
    subscriber = rabbit_repository.broker.subscriber("AIResponse")

    # apply it to your handler
    subscriber(endpoints.handle_task)