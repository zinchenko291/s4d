from logging_setup import setup_logging
from app.agent import Agent
from app import Prompt
from app.utils.models import RequestModel, ResponseModel
from config import app_config

import asyncio
from faststream import FastStream
from faststream.rabbit import RabbitBroker
import logging


SERVICE_NAME="MCP-Agent"

setup_logging()
logger = logging.getLogger(__name__)
broker = RabbitBroker(f"amqp://{app_config.rabbit_user}:{app_config.rabbit_pass}@{app_config.rabbit_host}:{app_config.rabbit_port}/")
app = FastStream(broker)

agent = Agent(
    model=app_config.yandex_agent_url,
    prompt=Prompt("static/prompts.yaml", "company"),
    api_key=app_config.yandex_agent_api_key,
    base_url=f"{app_config.yandex_base_assistant_url}/v1",
    project=app_config.yandex_project_id,
    temperature=0.3,
    max_output_tokens=1500
)


@broker.subscriber("MCPSearch")
@broker.publisher("Results")
async def GetTask(data: str) -> ResponseModel:
    data = RequestModel.model_validate_json(data)
    response = GetInfo(company=data.payload)
    if response is None:
        logger.exception(f"Информация не найдена: {dir(data)}, model response: {response}")
        return ResponseModel(
            id=data.id,
            status=False,
            sender=SERVICE_NAME)
    
    return ResponseModel(
        id=data.id,
        status=True,
        sender=SERVICE_NAME,
        payload=response)


def GetInfo(company: str) -> str:
    return agent.Ask(
        message=f"Компания: \"{company}\"",
        tools=[
            {
                "server_label": "hack-mcp",
                "server_url": "https://db8dstvb51nangpbbj7f.gs2td6d8.mcpgw.serverless.yandexcloud.net",
                "type": "mcp",
                "require_approval": "never",
                "metadata": {
                    "description": "Поиск компании в CRM"
                },

            }
        ]
    )

# print(GetInfo("ОГРН: 5067847031357"))
# print(GetInfo("Timeweb"))


if __name__ == "__main__":
    asyncio.run(app.run())
