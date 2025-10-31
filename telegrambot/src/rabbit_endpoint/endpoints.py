import json

from dependency_injector.wiring import inject, Provide

from src.application import dtos

from src import plugin, BaseRepository, Container
from src import shared_vars


async def handle_task(msg: str):
    msg = json.loads(msg)
    task_id = msg.get("id", "0")

    if not msg.get("status"):
        r = await shared_vars.base_repository.update_search_task(task_id, dtos.UpdateSearchTaskDto(summary=None,
                                                                                                   short_summary=None,
                                                                                                   status=1 if msg.get(
                                                                                                       "status") else -1))

        await plugin.bot.send_message(chat_id=r.value, text="<b>❌ Задача исполнена</b>\n\nИзвините, но мы не смогли найти информацию об этой компании.\n\n<i>Попробуйте переформулировать ваш запрос, возможно наш агент вас недопонял :3</i>")
        return



    payload = msg.get("payload", {})

    short_summary = payload.get("shortSummary", None)
    summary = payload.get("summary", None)

    r = await shared_vars.base_repository.update_search_task(task_id, dtos.UpdateSearchTaskDto(summary=summary, short_summary=short_summary, status=1 if msg.get("status") else -1))


    await plugin.bot.send_message(chat_id=r.value, text=f'<b>📔 Задача исполнена</b>\n\n{short_summary}\n\n<i><a href="s4d.zzvt.pw/{task_id}">Подробнее</a></i>')

