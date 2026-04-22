import feedparser

# -----------------------------
# HS-Code Klassifizierung (regelbasiert)
# -----------------------------

def classify_hs_code(text: str) -> str:
    t = text.lower()

    rules = [
        (["laptop", "notebook", "computer"], "847130"),
        (["phone", "smartphone", "handy"], "851712"),
        (["t-shirt", "shirt"], "610910"),
        (["shoes", "sneaker"], "640411"),
        (["plastic"], "392690"),
        (["steel"], "720839"),
    ]

    for keywords, code in rules:
        if any(k in t for k in keywords):
            return code

    return "999999"  # unbekannt / sonstige

# -----------------------------
# Währungsumrechnung + Zollwert
# -----------------------------

FX_RATES = {
    "EUR": 1.00,
    "USD": 0.92,
    "GBP": 1.15,
    "CHF": 1.04,
}

def convert_to_eur(price: float, currency: str) -> float:
    c = currency.upper()
    if c not in FX_RATES:
        raise ValueError("Unsupported currency")
    return price * FX_RATES[c]

def calculate_customs_value(price: float, currency: str, freight: float, insurance: float):
    price_eur = convert_to_eur(price, currency)
    customs_value = price_eur + freight + insurance
    return {
        "price_eur": round(price_eur, 2),
        "customs_value": round(customs_value, 2),
        "currency_used": "EUR",
    }

# -----------------------------
# Zoll-News (RSS-Feed)
# -----------------------------

def fetch_customs_news():
    # HIER KANNST DU SPÄTER ANDERE FEEDS EINTRAGEN
    feed = feedparser.parse("https://www.zoll.de/SiteGlobals/Functions/RSSFeed/RSSNewsfeed.xml")
    items = []
    for entry in feed.entries[:10]:
        items.append({
            "title": entry.title,
            "url": entry.link,
            "source": "Zoll.de"
        })
    return items
