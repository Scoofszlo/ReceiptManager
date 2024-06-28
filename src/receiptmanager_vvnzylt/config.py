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
        config_file = json.load(file)
        return config_file

def update_config(config_file):
    config_file = json.dumps(config_file, indent=4, ensure_ascii=False)
    with open("./program_data/receiptmanager.config", "w", encoding="utf-8") as file:
        file.write(config_file)
