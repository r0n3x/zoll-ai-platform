from fastapi import APIRouter
from ..fx_client import get_rates

router = APIRouter()

@router.post("/calculate")
async def calculate_customs_value(
    goods_value: float,
    goods_currency: str,
    freight: float = 0.0,
    insurance: float = 0.0,
    other_costs: float = 0.0,
):
    total_value = goods_value + freight + insurance + other_costs

    rates = await get_rates(base=goods_currency.upper())
    targets = ["EUR", "USD", "GBP", "CHF"]

    result = {}
    for cur in targets:
        if cur == goods_currency.upper():
            result[cur] = total_value
        else:
            rate = rates.get(cur)
            if rate:
                result[cur] = total_value * rate

    return {
        "base_currency": goods_currency.upper(),
        "total_value_base": total_value,
        "converted": result,
    }
