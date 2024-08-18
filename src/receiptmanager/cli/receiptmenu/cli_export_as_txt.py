from src.receiptmanager.constants import TXT_SAVED_RESULTS_FOLDER_PATH
from src.receiptmanager.receiptprocessor.general import is_receipt_list_empty
from src.receiptmanager.receiptprocessor.export_data import get_file_name_input, export_as_txt
from src.receiptmanager.utils import (
    clear_console,
    is_path_exists,
    create_folder_path
)

def display(receipt_obj):
    clear_console()

    if is_receipt_list_empty(receipt_obj):
        print("Cannot write results as there is nothing to export.")
        input("Press Enter to proceed...")
        return

    print(f"(Type \"CANCEL\" to go back)\n\nEnter file name. Type nothing to use default name (\"{receipt_obj.receipt_code}\"): ")
    file_name = get_file_name_input(receipt_obj, file_type="TXT")

    if not is_path_exists(TXT_SAVED_RESULTS_FOLDER_PATH):
        create_folder_path(TXT_SAVED_RESULTS_FOLDER_PATH)

    export_as_txt(receipt_obj, file_name)
