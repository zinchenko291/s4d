from aiogram import filters, types
from aiogram.fsm import scene, context
from dependency_injector.wiring import inject, Provide

from src.core import UserSession
from src.infrastructure.services import Translator
from src.presentation import tools
from src.container import Container

class MainScene(scene.Scene, reset_data_on_enter=False, reset_history_on_enter=True, callback_query_without_state=True):

    @scene.on.message.enter(Translator)
    @scene.on.callback_query.enter(Translator)
    @tools.request_handler(auth=True, bypass_if_command=True, category="menu")
    @inject
    async def default_handler(self, query: types.CallbackQuery or types.Message, translator: Translator = Provide[Container.translator], user: UserSession=None):
        # print("main -> user", user)
        # print("main -> user -> data", user.data)
        # print("main -> user -> data -> role", user.data.role)

        text = translator.translate("menu-text")
        return {"text": text}
