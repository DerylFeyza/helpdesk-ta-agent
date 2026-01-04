import httpx
import os
from src.exceptions import handle_httpx_errors

IDMT_BASE = os.getenv("IDMT_BASE_URL")
if IDMT_BASE is None:
    raise ValueError("Environment variable 'IDMT_BASE_URL' not set")


@handle_httpx_errors(service_name="IDMT", base_url=IDMT_BASE)
async def check_health() -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{IDMT_BASE}/health"
        response = await client.get(url)
        response.raise_for_status()
        result = response.json()
        return result
