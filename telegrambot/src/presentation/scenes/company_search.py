import aiogram

from aiogram import filters, types
from aiogram.fsm import scene, context
from dependency_injector.wiring import inject, Provide

from src import BaseRepository, RabbitRepository
from src.core import UserSession
from src.infrastructure.services import Translator
from src.presentation import tools
from src.container import Container

from src.application import dtos

category = "company_search"


class MainScene(scene.Scene, state="company_search"):

    @scene.on.message.enter()
    @scene.on.callback_query.enter()
    @tools.request_handler(auth=True, bypass_if_command=True, category=category)
    @inject
    async def default_handler(self, query: types.CallbackQuery or types.Message,
                              base_repository: BaseRepository = Provide[Container.base_repository],
                              rabbit_repository: RabbitRepository = Provide[Container.rabbit_repository],
                              translator: Translator = Provide[Container.translator], user: UserSession = None):
        prompt = (await self.wizard.get_data()).get("task_text")
        if not prompt:
            raise Exception("error-invalid_data-empty-task_text")

        result = await base_repository.register_search_task(dtos.SearchTaskDto(telegram_id=query.from_user.id, message_id=query.message_id))

        if not result.is_success:
            raise Exception("error-internal-database-error")

        await rabbit_repository.search_company_async(dtos.NewSearchTaskDto(id=result.value.id, request=prompt))

        text = translator.translate("company_search-queued-text")


        return {"text": text}
