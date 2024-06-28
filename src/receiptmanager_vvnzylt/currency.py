currency = [
    {
        "currency_word": None,
        "abbreviation": None,
        "symbol": None
    },
    {
        "currency_word": "Philippine Peso",
        "abbreviation": "PHP",
        "symbol": "₱"
    },
    {
        "currency_word": "Japanese Yen",
        "abbreviation": "JPY",
        "symbol": "¥"
    },
    {
        "currency_word": "United States Dollar",
        "abbreviation": "USD",
        "symbol": "$"
    },
    {
        "currency_word": "Euro",
        "abbreviation": "EUR",
        "symbol": "€"
    }
]

def get_currency(config):
    return config["currency"][0]["symbol"]
