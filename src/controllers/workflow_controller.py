from fastapi import status
from fastapi.responses import JSONResponse
from src.dto.workflow_dto import WorkflowParadiseRequest


class WorkflowController:
    @staticmethod
    async def process_paradise_workflow(request: WorkflowParadiseRequest):
        try:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Request processed successfully"},
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content={"error": str(e)}
            )
