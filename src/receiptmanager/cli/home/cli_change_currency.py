from src.receiptmanager.config import update_config
from src.receiptmanager.receiptprocessor.general import display_config
from src.receiptmanager.utils import clear_console

def display(config_file):
    clear_console()
    display_config(config_file)

    print("\n0 = Go back\n1 = Do not use currency\n2 = Use Philippine Peso\n3 = Use Japanese Yen\n4 = Use US Dollar\n5 = Use Euro")
    print("\nEnter option:")

    while True:
        try:
            option = int(input(">>> "))

            if option == 0:
                return
            if option == 1:
                config_file["currency"] = None
            elif option == 2:
                config_file["currency"] = "PHP"
            elif option == 3:
                config_file["currency"] = "JPY"
            elif option == 4:
                config_file["currency"] = "USD"
            elif option == 5:
                config_file["currency"] = "EUR"
            else:
                print("\nERROR: Invalid option. Please enter a number between 1 and 4.")
                continue
        except ValueError:
            print("\nERROR: Invalid value. Please enter a correct number.")
            continue

        update_config(config_file)
        clear_console()
        return
