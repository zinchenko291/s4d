from faststream.rabbit import RabbitBroker

from src.infrastructure.services import BaseRepository

rabbit_broker: RabbitBroker = None
base_repository: BaseRepository = None