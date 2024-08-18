from src.receiptmanager.receiptprocessor.edit_entry import (
    display_entry_details,
    get_entry_to_edit,
    get_new_item_name_input,
    get_new_quantity_input,
    get_new_unit_price_input,
    change_entry_name,
    change_entry_quantity,
    change_entry_unit_price,
    change_entry_total_price
    )
from src.receiptmanager.receiptprocessor.general import is_receipt_list_empty, display_entries, get_lowest_idx_pos, get_highest_idx_pos
from src.receiptmanager.utils import clear_console

def display(receipt_obj):
    clear_console()

    if is_receipt_list_empty(receipt_obj):
        print("\nERROR: Cannot edit as there is nothing to edit.")
        input("Press Enter to proceed...")
        return

    display_entries(receipt_obj)

    min_value = get_lowest_idx_pos(receipt_obj)
    max_value = get_highest_idx_pos(receipt_obj)

    print("\n(Type \"CANCEL\" to go back)\n\nType the position number of entry you want to change the details:")
    while True:
        try:
            position = str(input(">>> "))
            if position == "CANCEL":
                return
            else:
                position = int(position)

            if position >= min_value and position <= max_value:
                entry = get_entry_to_edit(position, receipt_obj)
                __display_cli_choose_option(entry)
            else:
                print("\nERROR: Please enter a valid number to change entry.")
                continue
        except ValueError:
            print("\nERROR: Please enter a valid number to change entry.")
            continue

        display_entries(receipt_obj)
        print("\n(Type \"CANCEL\" to go back)\n\nType the position number of entry you want to change the details:")

def __display_cli_choose_option(node):
    clear_console()
    display_entry_details(node)
    print("\nChoose option:\n0 = Go back\n1 = Edit item name\n2 = Edit quantity\n3 = Edit unit price\n\nChoose option:")
    while True:
        try:
            option = int(input(">>> "))
            if option == 0:
                return
            if option == 1:
                __display_cli_change_item_name(node)
            elif option == 2:
                __display_cli_change_quantity(node)
            elif option == 3:
                __display_cli_change_unit_price(node)
            else:
                print("\nERROR: Please enter a valid number between 0 and 3.")
        except ValueError:
            print("\nERROR: Please enter a valid number between 0 and 3.")

        display_entry_details(node)
        print("\nChoose option:\n0 = Go back\n1 = Edit item name\n2 = Edit quantity\n3 = Edit unit price\n\nChoose option:")

def __display_cli_change_item_name(node):
    clear_console()
    display_entry_details(node)

    print("\nEnter new item name:")
    new_name = get_new_item_name_input()

    print(f"\n\"{node.entry.item_name}\" will be changed into \"{new_name}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")

    while True:
        try:
            option = int(input(">>> "))
            if option == 1:
                change_entry_name(node, new_name)
                return
            elif option == 2:
                return
            else:
                print("\nERROR: Invalid option. Please enter a number between 1 and 2.")
        except ValueError:
            print("\nERROR: Invalid value. Please enter a correct number.")

def __display_cli_change_quantity(node):
    clear_console()
    display_entry_details(node)

    print("\nEnter new quantity:")
    new_quantity = get_new_quantity_input()

    print(f"\n{node.entry.item_name}\'s quantity will be changed from \"{node.entry.quantity}\" to \"{new_quantity}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")

    while True:
        try:
            option = int(input(">>> "))
            if option == 1:
                change_entry_quantity(node, new_quantity)
                change_entry_total_price(node, new_quantity, "CHANGE_QUANTITY")
                return
            elif option == 2:
                return
            else:
                print("\nERROR: Invalid option. Please enter a number between 1 and 2.")
        except ValueError:
            print("\nERROR: Invalid value. Please enter a correct number.")

def __display_cli_change_unit_price(node):
    clear_console()
    display_entry_details(node)

    print("\nEnter new unit price:")
    new_unit_price = get_new_unit_price_input()

    print(f"\n{node.entry.item_name}\'s unit price will be changed from \"{node.entry.unit_price}\" to \"{float(new_unit_price)}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")

    while True:
        try:
            option = int(input(">>> "))
            if option == 1:
                change_entry_unit_price(node, new_unit_price)
                change_entry_total_price(node, new_unit_price, "CHANGE_UNIT_PRICE")
                return
            elif option == 2:
                return
            else:
                print("\nERROR: Invalid option. Please enter a number between 1 and 2.")
        except ValueError:
            print("\nERROR: Invalid value. Please enter a correct number.")
