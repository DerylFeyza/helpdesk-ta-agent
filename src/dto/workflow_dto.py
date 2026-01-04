from pydantic import BaseModel


class WorkflowParadiseRequest(BaseModel):
    laborcode: str
    warehouse: list[str]
