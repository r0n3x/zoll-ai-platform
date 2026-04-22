import httpx
from .config import settings

async def classify_product_llm(description: str, technical_data: dict | None, candidates: list[dict]) -> dict:
    prompt = {
        "description": description,
        "technical_data": technical_data,
        "candidates": candidates,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            settings.AI_API_BASE_URL,
            headers={"Authorization": f"Bearer {settings.AI_API_KEY}"},
            json={"prompt": prompt}
        )
    resp.raise_for_status()
    return resp.json()
