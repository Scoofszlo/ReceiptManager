"""Functions that are run when program is initialized."""
import os
from src.receiptmanager.config import get_default_program_config
from src.receiptmanager.constants import DATA_FOLDER_PATH, CONFIG_FILE_PATH

def initialize_program_folder():
    if not os.path.exists(DATA_FOLDER_PATH):
        os.makedirs(DATA_FOLDER_PATH)

def initialize_program_config():
    if not os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as file:
            file.write(get_default_program_config())
