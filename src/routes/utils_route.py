from fastapi import APIRouter, Request, Depends
from src.controllers.utils_controller import UtilsController
from src.model.credentials import CredentialType
from pydantic import BaseModel


utilsRouter = APIRouter(tags=["Utils"], prefix="/utils")


class CreateCredentialRequest(BaseModel):
    credential: str
    credential_type: CredentialType


@utilsRouter.post("/credentials/set")
async def set_credentials(
    request: Request, controller: UtilsController = Depends(UtilsController)
):
    form_data = dict(await request.form())
    return await controller.set_credentials(form_data)
