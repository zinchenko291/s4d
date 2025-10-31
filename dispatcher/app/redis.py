import redis.asyncio as aioredis
from typing import Optional, Any
import json
import logging

logger = logging.getLogger(__name__)


class RedisClient:
    async def connect(
        self, host: str, port: int,
        password: str, db: int):

        self._redis = await aioredis.from_url(
            f"redis://:{password}@{host}:{port}/{db}",
            encoding="utf-8", decode_responses=True,
            max_connections=10)

        logger.info("Инициализация Redis завершена")
    

    @classmethod
    async def new(
        cls, host: str, port: int,
        password: str, db: int) -> "RedisClient":
        obj = cls()
        await obj.connect(
            host=host, port=port,
            password=password, db=db)
        return obj
    

    async def set(
        self, key: str, value: Any, 
        ex: int = None) -> bool:
        return await self._redis.set(key, value, ex=ex)

    async def get(self, key: str) -> Optional[str]:
        return await self._redis.get(key)
    
    async def delete(self, *keys: str) -> int:
        return await self._redis.delete(*keys)
    
    async def exists(self, *keys: str) -> int:
        return await self._redis.exists(*keys)
    
    async def ttl(self, key: str) -> int:
        return await self._redis.ttl(key)
    
    async def set_json(self, key: str, value: dict, ex: int = None) -> bool:
        return await self.set(key, json.dumps(value), ex=ex)
    
    async def get_json(self, key: str) -> Optional[dict]:
        value = await self.get(key)
        return json.loads(value) if value else None
    
    
    