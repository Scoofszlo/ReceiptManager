import os
from receiptmanager_scoofszlo.config import get_default_program_config

def initialize_program_folder():
    program_folder = "./program_data/"

    if not os.path.exists(program_folder):
        os.makedirs(program_folder)

def initialize_program_config():
    config_file = "./program_data/receiptmanager.config"

    if not os.path.exists(config_file):
        with open(config_file, "w", encoding="utf-8") as file:
            file.write(get_default_program_config())

initialize_program_folder()
initialize_program_config()
