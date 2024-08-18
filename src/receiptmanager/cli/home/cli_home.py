"""The main user interface when the program is run."""
from src.receiptmanager.cli.home import (
    cli_change_config,
    cli_import_using_json,
    cli_import_using_txt
)
from src.receiptmanager.cli.receiptmenu import cli_menu
from src.receiptmanager.receipt_entry import ReceiptEntryList
from src.receiptmanager.utils import clear_console

def run():
    __display_message()
    print("\nEnter option:")

    while True:
        try:
            option = int(input(">>> "))

            if option == 1:
                cli_import_using_json.display()
            elif option == 2:
                cli_import_using_txt.display()
            elif option == 3:
                receipt_obj = ReceiptEntryList()
                cli_menu.display(receipt_obj)
            elif option == 4:
                cli_change_config.display()
            elif option == 5:
                input("\nPress Enter to exit...")
                break
            else:
                print("\nERROR: Invalid option. Please enter a number between 1 and 5.")
                continue
        except ValueError:
            print("\nERROR: Invalid value. Please enter a correct number.")
            continue

        __display_message()
        print("\nEnter option:")

def __display_message():
    clear_console()
    print("Welcome to ReceiptManager!")
    print("Please choose a number on what you want to do:\n1 = Import a receipt list using .JSON file\n2 = Import a receipt list using .TXT file (LEGACY)\n3 = Create a receipt list (manually)\n4 = Change program setitngs\n5 = Exit")
