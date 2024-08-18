
from src.receiptmanager.cli.receiptmenu import (
    cli_add_entry,
    cli_delete_entry,
    cli_edit_entry,
    cli_sort_list,
    cli_edit_receipt_header,
    cli_export_as_txt,
    cli_export_as_json
)
from src.receiptmanager.receiptprocessor.general import display_entries

def display(receipt_obj):
    __display_menu(receipt_obj)
    print("\nEnter option:")

    while True:
        try:
            option = int(input(">>> "))

            if option == 0:
                return
            elif option == 1:
                cli_add_entry.display(receipt_obj)
            elif option == 2:
                cli_delete_entry.display(receipt_obj)
            elif option == 3:
                cli_edit_entry.display(receipt_obj)
            elif option == 4:
                cli_sort_list.display(receipt_obj)
            elif option == 5:
                cli_edit_receipt_header.display(receipt_obj)
            elif option == 6:
                cli_export_as_txt.display(receipt_obj)
            elif option == 7:
                cli_export_as_json.display(receipt_obj)
            else:
                print("\nInvalid option. Please enter a number between 0 and 7.")
                continue
        except ValueError:
            print("\nInvalid value. Please enter a correct number.")
            continue

        __display_menu(receipt_obj)
        print("\nEnter option:")

def __display_menu(receipt_obj):
    display_entries(receipt_obj)
    print("\nChoose option:\n0 = Go back\n1 = Add entry\n2 = Delete entry\n3 = Edit entry details\n4 = Sort list\n5 = Change receipt header\n6 = Export as .TXT file (for formatted results)\n7 = Export as .JSON file (for importing)")
