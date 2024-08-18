from src.receiptmanager.receiptprocessor.general import (
    is_receipt_list_empty,
    display_entries,
    get_valid_positions,
    is_in_valid_positions
)
from src.receiptmanager.receiptprocessor.delete_entry import delete_entry
from src.receiptmanager.utils import clear_console

def display(receipt_obj):
    clear_console()

    if is_receipt_list_empty(receipt_obj):
        print("\nERROR: Cannot delete as there is nothing to delete.")
        input("Press Enter to proceed...")
        return

    display_entries(receipt_obj)
    valid_positions = get_valid_positions(receipt_obj) # Gets the valid positions of each entry that can be deleted

    print("\n(Type \"CANCEL\" to go back)\n\nType the position number of item you want to delete: ")

    while True:
        try:
            position = str(input(">>> "))
            if position == "CANCEL":
                return
            else:
                position = int(position)

            if is_in_valid_positions(position, valid_positions):
                delete_entry(receipt_obj, position)
                valid_positions = get_valid_positions(receipt_obj) # This is called again to update the valid positions since deletion was done
            else:
                print("\nERROR: Please enter a valid number to delete.")
                continue
        except ValueError:
            print("\nERROR: Please enter a valid number to delete.")
            continue

        if is_receipt_list_empty(receipt_obj):
            clear_console()
            print("\nINFO: There are no entries left as of all the entries have been deleted.")
            input("Press Enter to proceed...")
            return

        display_entries(receipt_obj)
        print("\n(Type \"CANCEL\" to go back)\n\nType the position number of item you want to delete: ")
