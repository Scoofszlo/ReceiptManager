from src.receiptmanager.cli.receiptmenu import cli_menu
from src.receiptmanager.constants import TXT_SAVED_RESULTS_FOLDER_PATH
from src.receiptmanager.receiptprocessor.import_data import get_valid_txt_file, import_using_txt
from src.receiptmanager.utils import clear_console

def display():
    clear_console()

    print("(Type \"CANCEL\" to go back)\n\nEnter file name:")
    txt_file = get_valid_txt_file()

    if txt_file is not None:
        with open(TXT_SAVED_RESULTS_FOLDER_PATH + txt_file + ".txt", "r", encoding="utf-8") as file:
            receipt_obj = import_using_txt(file)
            cli_menu.display(receipt_obj)

    return
