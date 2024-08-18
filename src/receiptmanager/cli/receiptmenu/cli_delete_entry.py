from src.receiptmanager.receiptprocessor.general import is_receipt_list_empty, display_entries, get_lowest_idx_pos, get_highest_idx_pos
from src.receiptmanager.receiptprocessor.delete_entry import delete_entry
from src.receiptmanager.utils import clear_console

def display(receipt_obj):
    clear_console()

    if is_receipt_list_empty(receipt_obj):
        print("\nERROR: Cannot delete as there is nothing to delete.")
        input("Press Enter to proceed...")
        return

    display_entries(receipt_obj)
    min_value = get_lowest_idx_pos(receipt_obj)
    max_value = get_highest_idx_pos(receipt_obj)

    print("\n(Type \"CANCEL\" to go back)\n\nType the position number of item you want to delete: ")

    while True:
        try:
            position = str(input(">>> "))
            if position == "CANCEL":
                return
            else:
                position = int(position)

            if position >= min_value and position <= max_value:
                delete_entry(receipt_obj, position)
            else:
                print("\nERROR: Please enter a valid number to delete.")
                continue
        except ValueError:
            print("\nERROR: Please enter a valid number to delete.")
            continue

        display_entries(receipt_obj)
        print("\n(Type \"CANCEL\" to go back)\n\nType the position number of item you want to delete: ")
