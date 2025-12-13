from fastapi import (
    APIRouter,
    status,
)
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.agents.scmt_agent import agent

chatRouter = APIRouter(tags=["Chat"])


class ChatRequest(BaseModel):
    chat: str


@chatRouter.post("/chat")
async def chat(request: ChatRequest):
    try:
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": request.chat}]}
        )

        last_message = result["messages"][-1]
        response_text = (
            last_message.content
            if hasattr(last_message, "content")
            else str(last_message)
        )

        thought_process = []
        for msg in result["messages"]:
            msg_dict = {
                "type": msg.__class__.__name__,
            }

            if hasattr(msg, "content"):
                msg_dict["content"] = msg.content

            if hasattr(msg, "tool_calls") and msg.tool_calls:
                msg_dict["tool_calls"] = [
                    {"name": tc.get("name"), "args": tc.get("args"), "id": tc.get("id")}
                    for tc in msg.tool_calls
                ]

            if hasattr(msg, "name"):
                msg_dict["tool_name"] = msg.name

            thought_process.append(msg_dict)

        return {"response": response_text, "thought_process": thought_process}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"error": str(e)}
        )
