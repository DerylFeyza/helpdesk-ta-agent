from fastapi import APIRouter
from src.controllers.workflow_controller import WorkflowController
from src.dto.workflow_dto import WorkflowParadiseRequest

workflowRouter = APIRouter(tags=["Chat"])


@workflowRouter.post("/workflow/paradise")
async def paradise_workflow(request: WorkflowParadiseRequest):
    return await WorkflowController.process_paradise_workflow(request)
