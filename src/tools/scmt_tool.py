from src.dto.scmt_dto import AssignTechnicianWarehouseSchema
from src.services.scmt_service import (
    get_SCMT_technician_details,
    assign_SCMT_technician_warehouse,
)
from langchain.tools import tool


@tool
async def get_scmt_technician_details_tool(technician_code: int) -> dict:
    """Search the SCMT system for technician details and its registered warehouse.

    Args:
        technician_code: technician identifier in SCMT system, either 8 digit or 6 digit code.
    """
    return await get_SCMT_technician_details(technician_code)


@tool
async def assign_scmt_warehouse(data: list[AssignTechnicianWarehouseSchema]) -> dict:
    """assign a new warehouse to technician in SCMT.

    Args:
        data: List of dictionaries containing technician_code and new_warehouse
              Example: [{"technician_code": "95157566", "new_warehouse": "WH-230601-172250-951479000"},{"technician_code": "12345678", "new_warehouse": "WH-230601-172250-951479000"}]

    Returns:
        dict: Response from SCMT API
    """
    return await assign_SCMT_technician_warehouse(data)
