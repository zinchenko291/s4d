from httpx import AsyncClient
from typing import List, Optional
import logging
import asyncio


logger = logging.getLogger(__name__)


class Search(AsyncClient):
    def __init__(
            self, api_token: str, base_url: str,
            folder_id: str, agent_id: str):
        self.folder_id = folder_id
        self.agent_id = agent_id


        super().__init__(
            headers={
                "Authorization": f"Api-Key {api_token}"
            },
            base_url=base_url
        )


    @classmethod
    async def new(
        cls, api_token: str, base_url: str,
        folder_id: str, agent_id: str,
        sites: List[str] = []) -> "Search":

        obj = cls(
            api_token=api_token, base_url=base_url,
            folder_id=folder_id, agent_id=agent_id)
        
        await obj.AgentInit(sites=sites)

        return obj


    
    async def AgentInit(self, sites: List[str]) -> None:
        await self.PingAgent()

        response = await self.patch(
            url=f"/assistants/v1/assistants/{self.agent_id}",
            json={
                "updateMask": {
                    "paths": ["tools"]
                },
                "tools": [
                    {
                    "genSearch": {
                        "options": {
                            "site": { "site": sites } if len(sites) > 0 else None,
                            "enableNrfmDocs": True
                        },
                        "description": "Инструмент для получения информации про указанную компанию"
                        }
                    }
                ]
            },
            headers={
                "Content-Type": "application/json"
            }   
        )

        if response.status_code != 200:
            logger.error(f"Ошибка настройки агента. Code: {response.status_code} data: {response.json()}")
            raise RuntimeError("Agent init error")

        logger.info(f"Агент: {self.agent_id} успешно настроен")



    async def PingAgent(self) -> None:
        response = await self.get(
            url=f"/assistants/v1/assistants/{self.agent_id}"
        )
        if response.status_code != 200:
            logger.error(f"Ошибка инициализации агента. Code: {response.status_code} data: {response.json()}")
            raise RuntimeError("Agent init error")


    async def CreateThread(self) -> Optional[str]:
        response = await self.post(
            url="/assistants/v1/threads",
            json={
                "folderId": self.folder_id 
            }
        )

        if response.status_code < 400:
            return response.json()["id"]
        else:
            logger.error(f"Ошибка создания треда. Code: {response.status_code} Message: {response.json()}")
            return None


    async def PostMessage(self, company: str, thread_id: str) -> Optional[str]:
        response = await self.post(
            url="/assistants/v1/messages",
            json={
                "threadId": thread_id,
                "content": {
                    "content": [
                    {
                        "text": {
                            "content": f"Компания: {company}"
                        }
                    }
                    ]
                }
            }
        )

        if response.status_code < 400:
            return response.json()["id"]
        else:
            logger.error(f"Ошибка создания сообщения. Code: {response.status_code} Message: {response.json()}")
            return None


    async def RunTask(self, thread_id: str) -> str:
        response = await self.post(
            url="/assistants/v1/runs",
            json={
                "assistantId": self.agent_id,
                "threadId": thread_id
            }
        )

        if response.status_code < 400:
            return response.json()["id"]
        else:
            logger.error(f"Ошибка создания задачи. Code: {response.status_code} Message: {response.json()}")
            return None
        

    async def Ask(
            self, company: str, retries_limit: int = 20,
            retry_delta: float = 1.5) -> Optional[str]:
        logger.info("Запуск поиска информации по компании")

        thread_id = await self.CreateThread()
        await self.PostMessage(company, thread_id)
        task_id = await self.RunTask(thread_id)
        retries = 0
        is_done = False

        while not is_done:
            response = await self.get(
                url=f"/assistants/v1/runs/{task_id}"
            )

            if response.status_code < 400:
                
                state = response.json()["state"]["status"]

                if state == "COMPLETED":
                    message = response.json()["state"]["completed_message"]["content"]["content"][0]["text"]["content"]
                    break
                elif state == "FAILED":
                    logger.error(f"Ошибка запроса: {response.json()}")
                    return None

            else:
                logger.error(f"Ошибка просмотра данных сообщения. Code: {response.status_code} Message: {response.json()}")
                return None
            
            if retries >= retries_limit:
                message = None
                logger.info(f"Превышено время ожидания запроса. Количесво попыток: {retries}, дельта: {retry_delta}")
                break

            retries += 1
            await asyncio.sleep(retry_delta)
            
        logger.info(f"Поиск информации завершен. Количесво попыток: {retries}, дельта: {retry_delta}")
        return message

