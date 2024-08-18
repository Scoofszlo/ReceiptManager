from src.receiptmanager.receiptprocessor.sort_list import (
    sort_by_item_name,
    sort_by_quantity,
    sort_by_unit_price,
    sort_by_total_price
)
from src.receiptmanager.utils import clear_console

def display(receipt_obj):
    __display_message()
    print("\nEnter option:")

    while True:
        try:
            option = int(input(">>> "))

            if option == 0:
                return
            elif option == 1:
                sort_by_item_name(receipt_obj)
                break
            elif option == 2:
                sort_by_quantity(receipt_obj)
                break
            elif option == 3:
                sort_by_unit_price(receipt_obj)
                break
            elif option == 4:
                sort_by_total_price(receipt_obj)
                break
            else:
                print("\nERROR: Invalid option. Please enter a number between 0 and 4.")
                continue
        except ValueError:
            print("\nERROR: Invalid value. Please enter a correct number.")
            continue

def __display_message():
    clear_console()
    print("Choose option:\n0 = Go back\n1 = Sort by item name\n2 = Sort by quantity\n3 = Sort by unit price\n4 = Sort by total price")
