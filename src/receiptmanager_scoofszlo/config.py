import json
from receiptmanager_scoofszlo.currency import currency

def get_default_program_config():
    default_config = {
        "currency": [currency[0]]
    }

    json_file = json.dumps(default_config, indent=4, ensure_ascii=False)
    return json_file

def load_config():
    try:
        with open("./program_data/receiptmanager.config", "r", encoding="utf-8") as file:
            config_file = json.load(file)
            return config_file
    except FileNotFoundError:
        print("ERROR: receiptmanager.config is missing. Please ensure that the program_data folder and its contents are not being modified or accessed.")
        input("\nPress Enter to exit...")
        exit(0)

def update_config(config_file):
    config_file = json.dumps(config_file, indent=4, ensure_ascii=False)
    try:
        with open("./program_data/receiptmanager.config", "w", encoding="utf-8") as file:
            file.write(config_file)
    except FileNotFoundError:
        print("ERROR: receiptmanager.config is missing. Please ensure that the program_data folder and its contents are not being modified or accessed.")
        input("\nPress Enter to exit...")
        exit(0)
