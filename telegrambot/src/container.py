from dependency_injector import containers, providers

from src.infrastructure.services import BaseRepository, RabbitRepository
from src.infrastructure.services.translator import Translator
from src.infrastructure.config import Config


class Container(containers.DeclarativeContainer):
    config = providers.Singleton(Config)
    translator = providers.Singleton(Translator, config=config)

    base_repository = providers.Singleton(BaseRepository, config=config)
    rabbit_repository = providers.Singleton(RabbitRepository, config=config)