"""
Handles configuration-related operations such as initialization, update,
or loading of a configuration file
"""
import json
from src.receiptmanager.constants import CONFIG_FILE_PATH
from src.receiptmanager.exceptions import ConfigNotFoundError

def get_default_program_config():
    """ 
    Convert the default configuration dictionary to a JSON-formatted string
    with indentation for readability and ensure non-ASCII characters are preserved.
    """
    
    default_config = {
        "currency": None
    }

    config_file = json.dumps(default_config, indent=4, ensure_ascii=False)
    return config_file

def load_config():
    """
    Loads the config from the program_data folder
    """
    try:
        with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
            config_file = json.load(file)
            return config_file
    except FileNotFoundError as e:
        raise ConfigNotFoundError() from e

def update_config(config_file):
    """
    Updates the config located in the program_data folder
    """
    config_file = json.dumps(config_file, indent=4, ensure_ascii=False)
    try:
        with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as file:
            file.write(config_file)
    except FileNotFoundError as e:
        raise ConfigNotFoundError() from e
