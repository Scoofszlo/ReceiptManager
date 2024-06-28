from receiptmanager_vvnzylt.action_handler import choose_action
from receiptmanager_vvnzylt.utils import clear_console

def main():
    def display_message():
        clear_console()
        print("Welcome to ReceiptChecker!")
        print("Please choose a number on what you want to do:\n1 = Import a receipt list using .JSON file\n2 = Import a receipt list using .TXT file (LEGACY)\n3 = Create a receipt list (manually)\n4 = Exit")

    display_message()
    print("\nEnter option:")

    while True:
        try:
            option = int(input(">>> "))

            if option == 1:
                clear_console()
                choose_action("IMPORT_USING_JSON")
            elif option == 2:
                clear_console()
                choose_action("IMPORT_USING_TXT")
            elif option == 3:
                clear_console()
                choose_action("CREATE_MANUALLY")
            elif option == 4:
                input("\nPress Enter to exit...")
                break
            else:
                print("\nInvalid option. Please enter a number between 1 and 4.")
                continue
        except ValueError:
            print("\nInvalid value. Please enter a correct number.")
            continue

        display_message()
        print("\nEnter option:")

if __name__ == "__main__":
    main()
