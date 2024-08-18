"""
Stores essential data such as paths and variables to lessen
hard-coded values throughout the program
"""
DATA_FOLDER_PATH = "./program_data/"
CONFIG_FILE_PATH = DATA_FOLDER_PATH + "/receiptmanager.config"
JSON_SAVED_RESULTS_FOLDER_PATH = DATA_FOLDER_PATH + "/saved_results/json/"
TXT_SAVED_RESULTS_FOLDER_PATH = DATA_FOLDER_PATH + "/saved_results/txt/"

CURRENCY = {
    None: {
        "currency_word": None,
        "symbol": None
    },
    "PHP": {
        "currency_word": "Philippine Peso",
        "symbol": "₱"
    },
    "JPY": {
        "currency_word": "Japanese Yen",
        "symbol": "¥"
    },
    "USD": {
        "currency_word": "United States Dollar",
        "symbol": "$"
    },
    "EUR": {
        "currency_word": "Euro",
        "symbol": "€"
    }
}
