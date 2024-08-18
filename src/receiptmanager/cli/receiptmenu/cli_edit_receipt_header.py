from src.receiptmanager.receiptprocessor.edit_receipt_header import (
    display_receipt_header,
    get_new_receipt_code_input,
    get_new_date_input,
    get_new_time_input,
    parse_current_receipt_date,
    parse_current_receipt_time,
    format_date,
    format_time,
    change_receipt_code,
    change_receipt_date,
    change_receipt_time
)
from src.receiptmanager.utils import clear_console

def display(receipt_obj):
    display_receipt_header(receipt_obj)
    print("\nEnter option:")

    while True:
        try:
            chosen_option = int(input(">>> "))

            if chosen_option == 0:
                return
            elif chosen_option == 1:
                __display_cli_change_receipt_code(receipt_obj)
            elif chosen_option == 2:
                __display_cli_change_date(receipt_obj)
            elif chosen_option == 3:
                __display_cli_change_time(receipt_obj)
            else:
                print("\nERROR: Invalid option. Please enter a number between 0 and 3.")
                continue
        except ValueError:
            print("\nERROR: Invalid value. Please enter a correct number.")
            continue

        display_receipt_header(receipt_obj)
        print("\nEnter option:")

def __display_cli_change_receipt_code(receipt_obj):
    clear_console()

    print("(Type \"CANCEL\" to go back)\n\nEnter new receipt code:")
    new_receipt_code = get_new_receipt_code_input()
    if new_receipt_code == "CANCEL":
        return

    print(f"\n\"{receipt_obj.receipt_code}\" will be changed into \"{new_receipt_code}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")

    while True:
        try:
            option = int(input(">>> "))
            if option == 1:
                change_receipt_code(receipt_obj, new_receipt_code)
                return
            elif option == 2:
                return
            else:
                print("\nERROR: Invalid option. Please enter a number between 1 and 2.")
        except ValueError:
            print("\nERROR: Invalid value. Please enter a correct number.")

def __display_cli_change_date(receipt_obj):
    clear_console()

    print("(Type \"CANCEL\" to go back)\n\nEnter new date in YYYY/MM/DD format (e.g., 2024/05/20):")
    new_date = get_new_date_input()
    if new_date == "CANCEL":
        return

    current_date = parse_current_receipt_date(receipt_obj)
    if current_date is not None:
        print(f"\n\"{format_date(current_date)}\" will be changed into \"{format_date(new_date)}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")
    else:
        print(f"\nNew date will be \"{format_date(new_date)}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")

    while True:
        try:
            option = int(input(">>> "))
            if option == 1:
                change_receipt_date(receipt_obj, new_date)
                return
            elif option == 2:
                return
            else:
                print("\nERROR: Invalid option. Please enter a number between 1 and 2.")
        except ValueError:
            print("\nERROR: Invalid value. Please enter a correct number.")

def __display_cli_change_time(receipt_obj):
    clear_console()

    print("(Type \"CANCEL\" to go back)\n\nEnter new time in HH:MM:SS format (e.g., 20:01:59):")
    new_time = get_new_time_input()
    if new_time == "CANCEL":
        return

    current_time = parse_current_receipt_time(receipt_obj)
    if current_time is not None:
        print(f"\n\"{format_time(current_time)}\" will be changed into \"{format_time(new_time)}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")
    else:
        print(f"\nNew time will be \"{format_time(new_time)}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")

    while True:
        try:
            option = int(input(">>> "))
            if option == 1:
                change_receipt_time(receipt_obj, new_time)
                return
            elif option == 2:
                return
            else:
                print("\nERROR: Invalid option. Please enter a number between 1 and 2.")
        except ValueError:
            print("\nERROR: Invalid value. Please enter a correct number.")
