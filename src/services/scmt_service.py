import httpx
import os
from src.dto.scmt_dto import AssignTechnicianWarehouseSchema
from src.exceptions import handle_httpx_errors

SCMT_BASE = os.getenv("SCMT_BASE_URL")


@handle_httpx_errors(service_name="SCMT", base_url=SCMT_BASE)
async def get_SCMT_technician_details(technician_id: int) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{SCMT_BASE}/scmt/technician/{technician_id}"
        response = await client.get(url)
        response.raise_for_status()
        result = response.json()

        if result.get("success") and result.get("data"):
            data = result["data"]

            warehouses = [
                {
                    "code": wh.get("location_id_destination_code"),
                    "name": wh.get("location_id_destination_description"),
                }
                for wh in data.get("warehouses", [])
            ]

            return {
                "success": True,
                "data": {
                    "technician_code": data.get("location_code"),
                    "status": data.get("location_status"),
                    "ktp": data.get("ktp"),
                    "warehouses": warehouses,
                },
            }

        return result


@handle_httpx_errors(service_name="SCMT", base_url=SCMT_BASE)
async def assign_SCMT_technician_warehouse(
    data: list[AssignTechnicianWarehouseSchema],
) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{SCMT_BASE}/scmt/warehouse"
        payload = {"data": data}
        response = await client.post(url, json=payload)
        response.raise_for_status()
        result = response.json()

        return result


@handle_httpx_errors(service_name="SCMT", base_url=SCMT_BASE)
async def get_SCMT_upload_output(output_id: str) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{SCMT_BASE}/scmt/result?output_number={output_id}"
        response = await client.get(url)
        response.raise_for_status()
        result = response.json()

        if result.get("success") and result.get("data"):
            data = result["data"]
            details_obj = data.get("details", {})
            all_details = []
            for detail in details_obj.get("inprocess", []):
                all_details.append(
                    {
                        "technician_code": detail.get("technician_code"),
                        "assigned_warehouse": detail.get("new_warehouse_code"),
                        "status": "inprocess",
                        "message": detail.get("remarks"),
                    }
                )

            for detail in details_obj.get("success", []):
                all_details.append(
                    {
                        "technician_code": detail.get("technician_code"),
                        "assigned_warehouse": detail.get("new_warehouse_code"),
                        "status": "success",
                        "message": detail.get("remarks"),
                    }
                )

            for detail in details_obj.get("error", []):
                all_details.append(
                    {
                        "technician_code": detail.get("technician_code"),
                        "assigned_warehouse": detail.get("new_warehouse_code"),
                        "status": "error",
                        "message": detail.get("remarks"),
                    }
                )

            return {
                "success": True,
                "data": {
                    "output_id": data.get("output_number"),
                    "process_status": data.get("process_status"),
                    "details": all_details,
                },
            }

        return result
