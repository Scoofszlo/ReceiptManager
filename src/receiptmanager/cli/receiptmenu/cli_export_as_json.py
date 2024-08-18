from src.receiptmanager.constants import JSON_SAVED_RESULTS_FOLDER_PATH
from src.receiptmanager.receiptprocessor.general import is_receipt_list_empty
from src.receiptmanager.receiptprocessor.export_data import get_file_name_input, export_as_json
from src.receiptmanager.utils import (
    clear_console,
    is_path_exists,
    create_folder_path
)

def display(receipt_obj):
    clear_console()

    if is_receipt_list_empty(receipt_obj):
        print("Cannot export as there is nothing to export.")
        input("Press Enter to proceed...")
        return

    print(f"(Type \"CANCEL\" to go back)\n\nEnter file name. Type nothing to use default name (\"{receipt_obj.receipt_code}\"): ")
    file_name = get_file_name_input(receipt_obj, file_type="JSON")

    if not is_path_exists(JSON_SAVED_RESULTS_FOLDER_PATH):
        create_folder_path(JSON_SAVED_RESULTS_FOLDER_PATH)

    export_as_json(receipt_obj, file_name)
