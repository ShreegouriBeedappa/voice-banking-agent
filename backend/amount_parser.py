
import re

ONES = {
    "zero": 0, "ek": 1, "do": 2, "teen": 3,
    "char": 4, "chaar": 4, "paanch": 5,
    "cheh": 6, "chhe": 6, "saat": 7,
    "aath": 8, "nau": 9, "das": 10,
    "gyarah": 11, "barah": 12, "terah": 13,
    "chaudah": 14, "pandrah": 15, "solah": 16,
    "satrah": 17, "atharah": 18, "unnis": 19,
    "bees": 20, "tees": 30, "chalis": 40,
    "pachaas": 50, "saath": 60, "sattar": 70,
    "assi": 80, "nabbe": 90,
}

def parse_amount(text: str):
    text = text.lower().replace(",", "").strip()

    match = re.search(
        r"\b(\d+(?:\.\d{1,2})?)\s*(?:rupees?|rs\.?|inr)?\b",
        text,
    )
    if match:
        value = float(match.group(1))
        return round(value, 2) if value > 0 else None

    special = {
        "dhai sau": 250,
        "dedh sau": 150,
        "dedh hazaar": 1500,
        "sawa do lakh": 225000,
        "dhai lakh": 250000,
        "dedh lakh": 150000,
        "ek lakh": 100000,
    }

    for phrase, value in special.items():
        if phrase in text:
            return value

    words = re.findall(r"[a-z]+", text)
    total = 0
    current = 0

    ignored = {
        "transfer", "send", "money", "pay", "please",
        "to", "the", "rupee", "rupees", "rs", "inr"
    }

    for word in words:
        if word in ignored:
            continue
        elif word == "sau":
            current = max(current, 1) * 100
        elif word in {"hazaar", "hazar"}:
            total += max(current, 1) * 1000
            current = 0
        elif word in {"lakh", "lac"}:
            total += max(current, 1) * 100000
            current = 0
        elif word in ONES:
            current += ONES[word]
        else:
            return None

    result = total + current
    return result if result > 0 else None
