# utils.py
# Utility functions for LUDARA AI backend



import re

# ---------------------------------------------------------
# HS CODE CLASSIFIER (simple rule-based fallback)
# ---------------------------------------------------------

def classify_hs_code(text: str) -> str:
    """
    Very simple rule-based HS classifier.
    Replace with real model or API later.
    """

    t = text.lower()

    # Example rules
    if "laptop" in t or "notebook" in t:
        return "847130"
    if "phone" in t or "smartphone" in t or "handy" in t:
        return "851712"
    if "t-shirt" in t or "shirt" in t:
        return "610910"
    if "shoes" in t or "sneaker" in t:
        return "640411"
    if "plastic" in t:
        return "392690"
    if "steel" in t:
        return "720839"

    # Fallback
    return "000000"


# ---------------------------------------------------------
# CUSTOMS VALUE CALCULATOR
# ---------------------------------------------------------

def calculate_customs_value(price: float, currency: str, freight: float, insurance: float):
    """
    Basic customs value calculator.
    """

    # Currency conversion (example rates)
    rates = {
        "EUR": 1.00,
        "USD": 0.92,
        "GBP": 1.15,
        "CHF": 1.04
    }

    currency = currency.upper()

    if currency not in rates:
        return {"error": "Unsupported currency"}

    # Convert to EUR
    price_eur = price * rates[currency]

    customs_value = price_eur + freight + insurance

    return {
        "price_eur": round(price_eur, 2),
        "customs_value": round(customs_value, 2),
        "currency_used": "EUR"
    }
