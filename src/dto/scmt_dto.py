from typing import TypedDict
from pydantic import BaseModel


class AssignTechnicianWarehouseSchema(TypedDict):
    technician_code: str
    new_warehouse: str


class ChatRequest(BaseModel):
    chat: str
