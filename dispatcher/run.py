from logging_setup import setup_logging
from app.utils.models import (
    RequestModel, ResponseModel,
    Result, Task, Payload, Sender,
    ResultPayload)
from config import app_config
from app.redis import RedisClient

from typing import Any
from faststream import FastStream
from faststream.rabbit import RabbitBroker
import logging
import asyncio

setup_logging()


logger = logging.getLogger(__name__)

broker = RabbitBroker(f"amqp://{app_config.rabbit_user}:{app_config.rabbit_pass}"
                      f"@{app_config.rabbit_host}:{app_config.rabbit_port}/")

app = FastStream(broker)


async def redis_init():
    global redis_client

    redis_client = await RedisClient.new(
        host=app_config.redis_host,
        port=app_config.redis_port,
        password=app_config.redis_pass,
        db=app_config.redis_db)


async def main():
    await asyncio.gather(
        app.run(),
        redis_init()
    )


@broker.subscriber("Requests")
async def GetTask(data: RequestModel) -> None:
    if await redis_client.exists(data.id):
        logger.exception(f"Сообщение {data.id} уже в обработке")
        await broker.publish(
            message=Result(
                id=data.id,
                status=False,
                payload="Задача уже существует"
                ).model_dump_json(),
            queue="AIResponse")
        return

    new_task = Task(
            id=data.id,
            stage=0,
            request=data.payload,
            payload=Payload())

    await redis_client.set_json(
        key=data.id,
        value=new_task.model_dump())
        
        
    await broker.publish(
        message=RequestModel(
            id=new_task.id,
            payload=new_task.request
            ).model_dump_json(),
        queue="NumSearch")


@broker.subscriber("Results")
async def dispatch(data: ResponseModel) -> Any:
    logger.info(f"Получено сообщение {data.id} от {data.sender}")

    match data.sender:
        case Sender.NumAgent:
            await from_NumAgent(data)
        case Sender.MCPAgent:
            await from_MCPAgent(data)
        case Sender.SearchAgent:
            await from_SearchAgent(data)
        case Sender.Summary:
            await from_Summary(data)
        case Sender.GeneralSummary:
            await from_GeneralSummary(data)


# Stage 1
async def from_NumAgent(data: ResponseModel) -> None:
    if not data.status:
        logger.exception(f"Исключение: {data.payload}")
        await broker.publish(
            message=Result(
                id=data.id,
                status=False,
                payload=data.payload
                ).model_dump_json(),
            queue="AIResponse")
        return
    
    logger.info(f"Задача {data.id}, найдена информация {data.payload}")
    task = Task.model_validate(await redis_client.get_json(data.id))
    
    task.payload.num = data.payload
    task.stage += 1

    await redis_client.set_json(
        key=task.id,
        value=task.model_dump())
    
    await broker.publish(
        message=RequestModel(
            id=task.id,
            payload=data.payload
            ).model_dump_json(),
        queue="MCPSearch")

    logger.info(f"Сообщение {task.id} перенаправлено в MCPSearch")


# Stage 2
async def from_MCPAgent(data: ResponseModel) -> None:
    if not data.status:
        logger.exception(f"Исключение: {data.payload}")
        await broker.publish(
            message=Result(
                id=data.id,
                status=False,
                payload=data.payload
                ).model_dump_json(),
            queue="AIResponse")
        return
    logger.info(f"Задача {data.id}, найдена информация {data.payload}")
    task = Task.model_validate(await redis_client.get_json(data.id))
    
    task.payload.mcp_response = data.payload
    task.stage += 1

    await redis_client.set_json(
        key=task.id,
        value=task.model_dump())
    
    await broker.publish(
        message=RequestModel(
            id=task.id,
            payload=task.request
            ).model_dump_json(),
        queue="WebSearch")

    logger.info(f"Сообщение {task.id} перенаправлено в WebSearch")


# Stage 3
async def from_SearchAgent(data: ResponseModel) -> None:
    logger.info(f"Задача {data.id}, найдена информация {data.payload}")
    task = Task.model_validate(await redis_client.get_json(data.id))

    task.payload.web_search_response = data.payload
    task.stage += 1

    await redis_client.set_json(
        key=task.id,
        value=task.model_dump())

    await broker.publish(
        message=RequestModel(
            id=task.id,
            payload=task.request
            ).model_dump_json(),
        exchange="summary")

    logger.info(f"Сообщение {task.id} перенаправлено в FANOUT summary")


# Stage 4/5
async def from_Summary(data: ResponseModel) -> None:
    logger.info(f"Задача {data.id}, найдена информация {data.payload}")
    task = Task.model_validate(await redis_client.get_json(data.id))

    task.payload.summary = data.payload
    task.stage += 1

    if task.stage == 5:
        await broker.publish(
            message=Result(
                id=task.id,
                status=True,
                payload=ResultPayload(
                    shortSummary=task.payload.general_summary,
                    summary=task.payload.summary)
                ).model_dump_json(),
            queue="AIResponse"
        )
        await redis_client.delete(task.id)
        logger.info(f"Задача {task.id} завершена")

    await redis_client.set_json(
        key=task.id,
        value=task.model_dump())

    logger.info(f"Статус задачи {task.id} обновлен")


# Stage 4/5
async def from_GeneralSummary(data: ResponseModel) -> None:
    logger.info(f"Задача {data.id}, найдена информация {data.payload}")
    task = Task.model_validate(await redis_client.get_json(data.id))

    task.payload.general_summary = data.payload
    task.stage += 1

    if task.stage == 5:
        await broker.publish(
            message=Result(
                id=task.id,
                status=True,
                payload=ResultPayload(
                    shortSummary=task.payload.general_summary,
                    summary=task.payload.summary)
                ).model_dump_json(),
            queue="AIResponse"
        )
        await redis_client.delete(task.id)
        logger.info(f"Задача {task.id} завершена")

    await redis_client.set_json(
        key=task.id,
        value=task.model_dump())
    
    logger.info(f"Статус задачи {task.id} обновлен")


if __name__ == "__main__":
    asyncio.run(main())
