#from dotenv import load_dotenv
# load_dotenv()

import os

import asyncio

from dependency_injector.containers import WiringConfiguration

from src.container import Container
from src.presentation.bot import start_telegram_bot

from src.runner import runner
from src import rabbit_endpoint


async def main(container):
    await runner()
    await rabbit_endpoint.register_routes()
    await start_telegram_bot()


if __name__ == "__main__":
    container = Container()
    container.wiring_config = WiringConfiguration(packages=["src", ])
    container.wire()

    asyncio.run(main(container))