from src.dto.scmt_dto import AssignTechnicianWarehouseSchema
from src.services.scmt_service import (
    get_SCMT_technician_details,
    assign_SCMT_technician_warehouse,
    get_SCMT_upload_output,
)
from langchain.tools import tool
import re


@tool
async def get_scmt_technician_details_tool(technician_code: int) -> dict:
    """Get technician details and registered warehouses from SCMT.

    IMPORTANT: only use this tool once.

    Args:
        technician_code: 6-8 digit technician ID
    """
    return await get_SCMT_technician_details(technician_code)


@tool
async def assign_scmt_warehouse(msg: str) -> dict:
    """Assign warehouses to technicians in SCMT

    IMPORTANT: only use this tool once since it performs a bulk assignment detected from msg.

    Args:
        msg: input string containing technician codes and warehouse codes
    """
    detected_labor = [
        word for word in msg.split() if re.match(r"^[0-9]{6}$|^[0-9]{8}$", word)
    ]

    detected_warehouse = list(set(re.findall(r"\bWH-[A-Za-z0-9-]+\b|[A-Z]\d{3,}", msg)))

    data = []
    for tech in detected_labor:
        for wh in detected_warehouse:
            data.append(
                {
                    "technician_code": tech,
                    "warehouse_code": wh,
                }
            )

    upload_process_result = await assign_SCMT_technician_warehouse(data)
    if not upload_process_result.get("success"):
        return upload_process_result

    body = upload_process_result.get("data", {}).get("body", "")
    match = re.search(r"MT/\d{8}/\d+", body)

    if not match:
        return {
            "success": False,
            "error": "Could not extract upload number from response",
        }

    upload_number = match.group(0)
    upload_result = await get_SCMT_upload_output(upload_number)

    return upload_result
