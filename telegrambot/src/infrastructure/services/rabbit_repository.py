import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.application import dtos


class RabbitRepository:
    _instance = None

    def __new__(cls, config=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.broker = RabbitBroker(f"amqp://{config.RABBIT_USER}:{config.RABBIT_PASS}@{config.RABBIT_HOST}:{config.RABBIT_PORT}/")  # стандартный RabbitMQ URL
            cls._instance.app = FastStream(cls._instance.broker)
        return cls._instance

    def close(self):
        self.app.exit()
        self.broker.stop()

    async def connect(self):
        await self.broker.connect()
        asyncio.create_task(self.broker.start())

    async def search_company_async(self, dto: dtos.NewSearchTaskDto):
        print(f"Отправлено сообщение в брокер Requests: {dto.dump()}")
        await self.broker.publish(
            dto.dump(),
            queue="Requests",
        )
