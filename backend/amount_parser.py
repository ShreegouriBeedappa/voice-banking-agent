
import re

ONES = {
    "zero": 0,
    "ek": 1,
    "aik": 1,
    "do": 2,
    "teen": 3,
    "char": 4,
    "chaar": 4,
    "paanch": 5,
    "panch": 5,
    "cheh": 6,
    "chhe": 6,
    "saat": 7,
    "aath": 8,
    "nau": 9,
    "das": 10,
    "gyarah": 11,
    "barah": 12,
    "terah": 13,
    "chaudah": 14,
    "pandrah": 15,
    "solah": 16,
    "satrah": 17,
    "atharah": 18,
    "unnis": 19,
    "bees": 20,
    "tees": 30,
    "chalis": 40,
    "pachaas": 50,
    "saath": 60,
    "sattar": 70,
    "assi": 80,
    "nabbe": 90,
}


def parse_amount(text: str):
    if not isinstance(text, str):
        return None

    text = text.lower().replace(",", "").strip()

    # Remove an actual recipient phrase such as "to Rahul".
    # Do not split ordinary phrases such as "want to transfer".
    amount_text = re.sub(
        r"\bto\s+[a-z][a-z.'-]*(?:\s+[a-z][a-z.'-]*){0,2}\s*$",
        "",
        text,
    ).strip()

    # Numeric amounts.
    match = re.search(
        r"\b(\d+(?:\.\d{1,2})?)\s*(?:rupees?|rs\.?|inr)?\b",
        amount_text,
    )

    if match:
        value = float(match.group(1))
        return round(value, 2) if value > 0 else None

    # Common Indian number phrases.
    special = {
        "dhai sau": 250,
        "dhai so": 250,
        "dedh sau": 150,
        "dedh so": 150,
        "dedh hazaar": 1500,
        "dedh hajar": 1500,
        "sawa do lakh": 225000,
        "dhai lakh": 250000,
        "dedh lakh": 150000,
        "ek lakh": 100000,
    }

    for phrase, value in special.items():
        if phrase in amount_text:
            return value

    # Remove common transfer and currency words.
    cleaned = re.sub(
        r"\b(transfer|send|bhej|bhejo|bhejdo|money|please|"
        r"rupaye|rupya|rupees?|rs|inr|ko|mein|me|account|to)\b",
        " ",
        amount_text,
    )

    words = re.findall(r"[a-z]+", cleaned)

    total = 0
    current = 0
    found_number = False

    for word in words:
        if word == "sau":
            current = max(current, 1) * 100
            found_number = True

        elif word in {"hazaar", "hazar"}:
            total += max(current, 1) * 1000
            current = 0
            found_number = True

        elif word in {"lakh", "lac"}:
            total += max(current, 1) * 100000
            current = 0
            found_number = True

        elif word in ONES:
            current += ONES[word]
            found_number = True

    result = total + current

    if found_number and result > 0:
        return result

    return None
