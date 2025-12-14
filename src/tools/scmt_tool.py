from src.dto.scmt_dto import AssignTechnicianWarehouseSchema
from src.services.scmt_service import (
    get_SCMT_technician_details,
    assign_SCMT_technician_warehouse,
)
from langchain.tools import tool


@tool
async def get_scmt_technician_details_tool(technician_code: int) -> dict:
    """Get technician details and registered warehouses from SCMT.

    Args:
        technician_code: 6-8 digit technician ID
    """
    return await get_SCMT_technician_details(technician_code)


@tool
async def assign_scmt_warehouse(data: list[AssignTechnicianWarehouseSchema]) -> dict:
    """Assign warehouses to technicians in SCMT (supports bulk operations).

    IMPORTANT: Always verify with get_scmt_technician_details_tool first ONCE to check:
    1) Technician exists
    2) Warehouse not already assigned

    Args:
        data: List of assignments, e.g. [{"technician_code": "95157566", "new_warehouse": "WH-230601..."}]
    """
    return await assign_SCMT_technician_warehouse(data)
