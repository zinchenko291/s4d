from app.services import Search
from config import app_config
from app.utils.models import RequestModel, ResponseModel

from logging_setup import setup_logging
from faststream import FastStream
from faststream.rabbit import RabbitBroker
import logging
import asyncio
import json


SERVICE_NAME="Search-Agent"
TEMP_SERVICE_NAME="Num-Agent"


setup_logging()
logger = logging.getLogger(__name__)
broker = RabbitBroker(f"amqp://{app_config.rabbit_user}:{app_config.rabbit_pass}@{app_config.rabbit_host}:{app_config.rabbit_port}/")
app = FastStream(broker)


async def init_agents():
    global client_num
    global client_search
    global client_global_search

    client_num = await Search.new(
        api_token=app_config.yandex_agent_api_key,
        base_url=app_config.yandex_base_assistant_url,
        folder_id=app_config.yandex_project_id,
        sites=[
            "https://egrul.nalog.ru/",
            "https://spark-interfax.ru/"
        ],
        agent_id=app_config.yandex_info_agent_id
    )


    client_search = await Search.new(
        api_token=app_config.yandex_agent_api_key,
        base_url=app_config.yandex_base_assistant_url,
        folder_id=app_config.yandex_project_id,
        sites=[
            "https://ria.ru/",
            "https://www.bbc.com/news",
            "https://focus.kontur.ru/",
            "https://www.gazeta.ru/",
            "https://www.forbes.ru/"
        ],
        agent_id=app_config.yandex_search_agent_id
    )


    client_global_search = await Search.new(
        api_token=app_config.yandex_agent_api_key,
        base_url=app_config.yandex_base_assistant_url,
        folder_id=app_config.yandex_project_id,
        agent_id=app_config.yandex_global_search_agent_id
    )



@broker.subscriber("WebSearch")
@broker.publisher("Results")
async def GetTask(data: str) -> ResponseModel:
    data = RequestModel.model_validate_json(data)
    news = await client_search.Ask(data.payload)
    general = await client_global_search.Ask(data.payload)

    return ResponseModel(
        id=data.id,
        status=True,
        sender=SERVICE_NAME,
        payload=json.dumps(
            {
                "general_info": general,
                "last_news": news
            }
        )
    )


@broker.subscriber("NumSearch")
@broker.publisher("Results")
async def GetTask2(data: str) -> ResponseModel:
    data = RequestModel.model_validate_json(data)
    num = await client_num.Ask(company=data.payload)
    if num == "0":
        return ResponseModel(
            id=data.id,
            status=False,
            sender=TEMP_SERVICE_NAME)
    
    return ResponseModel(
        id=data.id,
        status=True,
        sender=TEMP_SERVICE_NAME,
        payload=num)


async def main():
    await asyncio.gather(
        app.run(),
        init_agents()
    )


if __name__ == "__main__":
    asyncio.run(main())

