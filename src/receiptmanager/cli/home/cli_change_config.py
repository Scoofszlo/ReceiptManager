from src.receiptmanager.cli.home import cli_change_currency
from src.receiptmanager.config import load_config
from src.receiptmanager.receiptprocessor.general import display_config
from src.receiptmanager.utils import clear_console

def display():
    config_file = load_config()
    __display_menu(config_file)
    print("\nEnter option:")

    while True:
        try:
            option = int(input(">>> "))

            if option == 0:
                return
            elif option == 1:
                clear_console()
                cli_change_currency.display(config_file)
            else:
                print("\nERROR: Invalid option. Please enter a number between 0 and 1.")
                continue
        except ValueError:
            print("\nERROR: Invalid value. Please enter a correct number.")
            continue

        __display_menu(config_file)
        print("\nEnter option:")

def __display_menu(config_file):
    clear_console()
    display_config(config_file)
    print("\nChoose option:\n0 = Go back\n1 = Change currency")
