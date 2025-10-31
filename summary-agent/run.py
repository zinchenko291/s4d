from logging_setup import setup_logging
from app.agent import Agent
from config import app_config
from app.utils.models import ResponseModel, RequestModel

from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitExchange, ExchangeType
import logging
import asyncio
import json


SERVICE_NAME="Summary"
TEMP_SERVICE_NAME="General-Summary"


setup_logging()
logger = logging.getLogger(__name__)
broker = RabbitBroker(f"amqp://{app_config.rabbit_user}:{app_config.rabbit_pass}@{app_config.rabbit_host}:{app_config.rabbit_port}/")
app = FastStream(broker)


exchange = RabbitExchange("summary", type=ExchangeType.FANOUT)


async def agent_init():
    global agent_summary
    global agent_general_summary

    agent_summary = await Agent.new(
        api_token=app_config.yandex_agent_api_key,
        base_url=app_config.yandex_base_assistant_url,
        folder_id=app_config.yandex_project_id,
        agent_id=app_config.yandex_summary_agent_id
    )

    agent_general_summary = await Agent.new(
        api_token=app_config.yandex_agent_api_key,
        base_url=app_config.yandex_base_assistant_url,
        folder_id=app_config.yandex_project_id,
        agent_id=app_config.yandex_general_summary_agent_id
    )


@broker.subscriber("Summary", exchange=exchange)
@broker.publisher("Results")
async def GetTask(data: str) -> ResponseModel:
    data = json.loads(data)
    data = RequestModel(**data)
    response = await agent_summary.Ask(data.payload)

    return ResponseModel(
        id=data.id,
        status=True,
        sender=SERVICE_NAME,
        payload=response)


@broker.subscriber("GeneralSummary", exchange=exchange)
@broker.publisher("Results")
async def GetTask2(data: str) -> ResponseModel:
    data = json.loads(data)
    data = RequestModel(**data)
    response = await agent_general_summary.Ask(data.payload)

    return ResponseModel(
        id=data.id,
        status=True,
        sender=TEMP_SERVICE_NAME,
        payload=response)


async def main():
    await asyncio.gather(
        app.run(),
        agent_init()
    )

if __name__ == "__main__":
    asyncio.run(main())
