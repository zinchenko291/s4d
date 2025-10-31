import os

import aiohttp

from src.application import dtos

class BaseRepository:
    _instance = None

    def __new__(cls, config=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.base_url = os.getenv("BASE_URL")
            cls._instance.session = aiohttp.ClientSession()
        return cls._instance

    async def close(self):
        await self.session.close()


    async def register_search_task(self, dto: dtos.SearchTaskDto) -> dtos.Result[dtos.RegisterSearchTaskResponseDto]:
        async with self.session.post(f"{self.base_url}/api/v1/Assignments/register", json=dto.dump()) as response:
            if response.status != 200:
                return dtos.Result(status_code=response.status)

            return dtos.Result(status_code=response.status, value=dtos.RegisterSearchTaskResponseDto(**(await response.json())))

    async def update_search_task(self, task_id, dto: dtos.UpdateSearchTaskDto) -> dtos.Result[str]:
        async with self.session.post(f"{self.base_url}/api/v1/Assignments/{task_id}", json=dto.dump()) as response:
            if response.status != 200:
                return dtos.Result(status_code=response.status)

            return dtos.Result(status_code=response.status, value=(await response.json()).get("telegramId", 0))
