import httpx
from .config import settings

async def get_rates(base: str = "EUR"):
    async with httpx.AsyncClient() as client:
        resp = await client.get(settings.FX_API_URL, params={"base": base})
    resp.raise_for_status()
    return resp.json()["rates"]
