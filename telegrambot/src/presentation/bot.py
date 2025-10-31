import aiogram

from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dependency_injector.wiring import inject, Provide

from src.infrastructure.config import Config
from src.container import Container

from src.presentation.commands import router as command_router

dispatcher = Dispatcher()

from aiogram.fsm.scene import SceneRegistry
from src.presentation import scenes

from . import deep_link

scene_register = SceneRegistry(dispatcher)
scene_register.register(scenes.main.MainScene)
scene_register.register(scenes.company_search.MainScene)

dispatcher.include_router(deep_link.start_router)
dispatcher.include_router(command_router)

from src.presentation.middlewares import album_middleware

dispatcher.message.middleware(album_middleware.AlbumMiddleware())

from . import plugin

@inject
async def start_telegram_bot(config: Config = Provide[Container.config]):
    tgbot = aiogram.Bot(token=config.BOT_TOKEN,
                    default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    plugin.bot = tgbot

    await dispatcher.start_polling(tgbot, skip_updates=True)