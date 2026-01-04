from fastapi import status
from fastapi.responses import JSONResponse
from src.agents.warehouse_agent import agent
from src.dto.scmt_dto import ChatRequest


class ChatController:
    @staticmethod
    async def process_chat(request: ChatRequest):
        """
        Process chat request and return agent response with thought process and token usage.

        Args:
            request: ChatRequest containing the chat message

        Returns:
            Dict with response, thought_process, and token_usage or JSONResponse with error
        """
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

            # Aggregate token usage from all AI messages
            total_input_tokens = 0
            total_output_tokens = 0
            total_tokens = 0

            thought_process = []
            for msg in result["messages"]:
                msg_dict = {
                    "type": msg.__class__.__name__,
                }

                if hasattr(msg, "content"):
                    msg_dict["content"] = msg.content

                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    msg_dict["tool_calls"] = [
                        {
                            "name": tc.get("name"),
                            "args": tc.get("args"),
                            "id": tc.get("id"),
                        }
                        for tc in msg.tool_calls
                    ]

                if hasattr(msg, "name"):
                    msg_dict["tool_name"] = msg.name

                if hasattr(msg, "usage_metadata") and msg.usage_metadata:
                    total_input_tokens += msg.usage_metadata.get("input_tokens", 0)
                    total_output_tokens += msg.usage_metadata.get("output_tokens", 0)
                    total_tokens += msg.usage_metadata.get("total_tokens", 0)

                thought_process.append(msg_dict)

            token_usage = {
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
                "total_tokens": total_tokens,
            }

            return {
                "response": response_text,
                "thought_process": thought_process,
                "token_usage": token_usage,
            }
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content={"error": str(e)}
            )
