import httpx
import os
from src.dto.scmt_dto import AssignTechnicianWarehouseSchema

SCMT_BASE = os.getenv("SCMT_BASE_URL")


async def get_SCMT_technician_details(technician_id: int) -> dict:
    try:
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

    except httpx.ConnectError as e:
        raise Exception(f"Cannot connect to SCMT server at {SCMT_BASE}: {str(e)}")
    except httpx.TimeoutException as e:
        raise Exception(f"Request to SCMT server timed out: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise Exception(
            f"SCMT API returned error {e.response.status_code}: {e.response.text}"
        )
    except Exception as e:
        raise Exception(f"Error fetching technician details: {str(e)}")


async def assign_SCMT_technician_warehouse(
    data: list[AssignTechnicianWarehouseSchema],
) -> dict:
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{SCMT_BASE}/scmt/warehouse"
            payload = {"data": data}
            response = await client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()

            return result

    except httpx.ConnectError as e:
        raise Exception(f"Cannot connect to SCMT server at {SCMT_BASE}: {str(e)}")
    except httpx.TimeoutException as e:
        raise Exception(f"Request to SCMT server timed out: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise Exception(
            f"SCMT API returned error {e.response.status_code}: {e.response.text}"
        )
    except Exception as e:
        raise Exception(f"Error updating technician warehouse: {str(e)}")


async def get_SCMT_upload_output(output_id: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{SCMT_BASE}/scmt/result?output_number={output_id}"
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

    except httpx.ConnectError as e:
        raise Exception(f"Cannot connect to SCMT server at {SCMT_BASE}: {str(e)}")
    except httpx.TimeoutException as e:
        raise Exception(f"Request to SCMT server timed out: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise Exception(
            f"SCMT API returned error {e.response.status_code}: {e.response.text}"
        )
    except Exception as e:
        raise Exception(f"Error fetching technician details: {str(e)}")
