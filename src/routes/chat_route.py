from fastapi import APIRouter
from src.controllers.chat_controller import ChatController
from src.dto.scmt_dto import ChatRequest

chatRouter = APIRouter(tags=["Chat"])


@chatRouter.post("/chat")
async def chat(request: ChatRequest):
    """Route handler for chat endpoint."""
    return await ChatController.process_chat(request)
