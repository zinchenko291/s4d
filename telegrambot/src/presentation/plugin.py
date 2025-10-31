import aiogram
from dependency_injector.wiring import inject, Provide

from src import MailType
from src.container import Container
from src.core import Mail
from src.infrastructure.services import Translator

bot: aiogram.Bot = None


@inject
async def send_company_search_result(mail: Mail, translator: Translator = Provide[Container.translator]) -> None:

    keyboard = [
        [aiogram.types.InlineKeyboardButton(text=translator.translate("ui-tag-search_more"), callback_data="menu")]
    ]

    text = translator.translate("hook-mail-verified-text").format()

    await bot.send_message(mail.recipient.telegram_id, text=text, reply_markup=aiogram.types.InlineKeyboardMarkup(inline_keyboard=keyboard))
