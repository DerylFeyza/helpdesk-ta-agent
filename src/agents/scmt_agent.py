from langchain.agents import create_agent
from src.tools.scmt_tool import get_scmt_technician_details_tool, assign_scmt_warehouse
from src.llm.llm import model


tools = [get_scmt_technician_details_tool, assign_scmt_warehouse]

system_prompt = """You are a helpdesk agent that helps users with technician warehouse management system.
If you are tasked with assigning warehouses, always check the registered warehouse again and make sure its registered.
If its not registered, do not assign it and inform the user.
If the user asks for unrelated things, politely refuse. Use the tools provided to you to get accurate information. Always think step by step.

If you do not know, say you do not know."""

agent = create_agent(
    model,
    tools,
    system_prompt=system_prompt,
)
