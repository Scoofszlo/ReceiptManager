import json
from receiptmanager_scoofszlo.utils import clear_console
from receiptmanager_scoofszlo.currency import currency
from receiptmanager_scoofszlo.config import update_config

def change_program_settings():
    def display_menu():
        display_options(config_file)
        print("\nChoose option:\n0 = Go back\n1 = Change currency")

    config_location = "./program_data/receiptmanager.config"
    try:
        with open(config_location, "r", encoding="utf-8") as file:
            config_file = json.load(file)
    except FileNotFoundError:
        print("ERROR: receiptmanager.config is missing. Please ensure that the program_data folder and its contents are not being modified or accessed.")
        input("\nPress Enter to exit...")
        exit(0)

    display_menu()
    print("\nEnter option:")

    while True:
        try:
            option = int(input(">>> "))

            if option == 0:
                return
            elif option == 1:
                clear_console()
                change_currency(config_file)
            else:
                print("\nERROR: Invalid option. Please enter a number between 1 and 4.")
                continue
        except ValueError:
            print("\nERROR: Invalid value. Please enter a correct number.")
            continue

        display_menu()
        print("\nEnter option:")

def display_options(config_file):
    if config_file["currency"][0]["currency_word"] is not None:
        print(f"\"currency\": {config_file["currency"][0]["abbreviation"]} ({config_file["currency"][0]["symbol"]}) - {config_file["currency"][0]["currency_word"]}")
    else:
        print("\"currency\": NO_CURRENCY_USED")

def change_currency(config_file):
    clear_console()
    print("0 = Go back\n1 = Do not use currency\n2 = Use Philippine Peso\n3 = Use Japanese Yen\n4 = Use US Dollar\n5 = Use Euro")
    print("\nEnter option:")

    while True:
        try:
            option = int(input(">>> "))

            if option == 0:
                clear_console()
                return
            if option == 1:
                config_file["currency"] = [currency[0]]
            elif option == 2:
                config_file["currency"] = [currency[1]]
            elif option == 3:
                config_file["currency"] = [currency[2]]
            elif option == 4:
                config_file["currency"] = [currency[3]]
            elif option == 5:
                config_file["currency"] = [currency[4]]
            else:
                print("\nERROR: Invalid option. Please enter a number between 1 and 4.")
                continue
        except ValueError:
            print("\nERROR: Invalid value. Please enter a correct number.")
            continue

        update_config(config_file)
        clear_console()
        return
