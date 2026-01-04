import os
from typing import Any, Dict, Optional
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.asynchronous.collection import AsyncCollection


class MongoDBHelper:
    def __init__(self):
        self.uri: str = os.getenv("DATABASE_URL")
        self._client: Optional[AsyncMongoClient[Dict[str, Any]]] = None
        self._db_name: str = os.getenv("DATABASE_NAME")

    @property
    def client(self) -> AsyncMongoClient[Dict[str, Any]]:
        if self._client is None:
            self._client = AsyncMongoClient(
                self.uri, maxPoolSize=100, minPoolSize=10, maxIdleTimeMS=60000
            )
        return self._client

    def get_db(self) -> AsyncDatabase[Dict[str, Any]]:
        return self.client[self._db_name]

    async def close(self):
        if self._client:
            await self._client.close()


db_helper = MongoDBHelper()
