from typing import TypeVar, Generic, Optional, Type
from bson import ObjectId
from src.model.credentials import CredentialsModel, CredentialType
from pydantic import BaseModel
from pymongo.asynchronous.database import AsyncDatabase

T = TypeVar("T", bound=BaseModel)


class BaseMongoRepository(Generic[T]):
    def __init__(self, db: AsyncDatabase, collection_name: str, model: Type[T]):
        self.collection = db[collection_name]
        self.model = model

    async def get_by_id(self, id: str) -> Optional[T]:
        doc = await self.collection.find_one({"_id": ObjectId(id)})
        return self.model.model_validate(doc) if doc else None

    async def create(self, model_instance: T) -> str:
        data = model_instance.model_dump(by_alias=True, exclude={"id"})
        result = await self.collection.insert_one(data)
        return str(result.inserted_id)


class InitializeMongoConstraints:
    def __init__(self, db: AsyncDatabase):
        self.db = db

    async def setup(self):
        print("Setting up MongoDB constraints...")
        cred_repo = CredentialRepository(self.db)
        await cred_repo.collection.create_index("credential_type", unique=True)
        print("MongoDB constraints set up.")


class CredentialRepository(BaseMongoRepository[CredentialsModel]):
    def __init__(self, db: AsyncDatabase):
        super().__init__(db, "credentials", CredentialsModel)

    async def find_by_type(
        self, cred_type: CredentialType
    ) -> Optional[CredentialsModel]:
        doc = await self.collection.find_one({"credential_type": cred_type.value})
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return self.model.model_validate(doc) if doc else None

    async def upsert(self, model_instance: CredentialsModel) -> CredentialsModel:
        data = model_instance.model_dump(by_alias=True, exclude={"id"})
        from pymongo import ReturnDocument

        cred_type_value = (
            model_instance.credential_type.value
            if isinstance(model_instance.credential_type, CredentialType)
            else model_instance.credential_type
        )

        result = await self.collection.find_one_and_update(
            {"credential_type": cred_type_value},
            {"$set": data},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )

        if result and "_id" in result:
            result["_id"] = str(result["_id"])

        return self.model.model_validate(result)
