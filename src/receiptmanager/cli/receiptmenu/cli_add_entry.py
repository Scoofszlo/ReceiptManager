from src.receiptmanager.receiptprocessor.add_entry import (
    get_item_name,
    get_quantity,
    get_unit_price,
    get_new_entry_idx_pos,
    add_entry
)
from src.receiptmanager.utils import clear_console

def display(receipt_obj):
    clear_console()

    while True:
        ctr = get_new_entry_idx_pos(receipt_obj)

        print("(Type \"DONE\" to stop adding entries)\n")
        print("Entry #", ctr, sep="")

        print("Enter item name: ")
        item_name = get_item_name()
        if not item_name:
            return

        print("\nEnter quantity:")
        quantity = get_quantity()
        if not quantity:
            return

        print("\nEnter unit price: ")
        unit_price = get_unit_price()
        if not unit_price:
            return

        add_entry(receipt_obj, item_name, quantity, unit_price, ctr)

        clear_console()
