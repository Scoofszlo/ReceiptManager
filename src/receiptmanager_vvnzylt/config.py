import json
from receiptmanager_vvnzylt.currency import currency

def get_default_program_config():
    default_config = {
        "currency": [currency[0]]
    }

    json_file = json.dumps(default_config, indent=4, ensure_ascii=False)
    return json_file

def load_config():
    with open("./program_data/receiptmanager.config", "r", encoding="utf-8") as file:
        json_file = json.load(file)
        return json_file
