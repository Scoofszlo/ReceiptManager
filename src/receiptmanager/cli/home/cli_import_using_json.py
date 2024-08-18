from src.receiptmanager.cli.receiptmenu import cli_menu
from src.receiptmanager.constants import JSON_SAVED_RESULTS_FOLDER_PATH
from src.receiptmanager.receiptprocessor.import_data import get_valid_json_file, import_using_json
from src.receiptmanager.utils import clear_console

def display():
    clear_console()

    print("(Type \"CANCEL\" to go back)\n\nEnter file name:")
    json_file = get_valid_json_file()

    if json_file is not None:
        with open(JSON_SAVED_RESULTS_FOLDER_PATH + json_file + ".json", "r", encoding="utf-8") as file:
            receipt_obj = import_using_json(file)
            cli_menu.display(receipt_obj)

    return
