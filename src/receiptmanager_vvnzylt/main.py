import re
import os
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from receiptmanager_vvnzylt.receipt_entry import ReceiptEntryList, ReceiptEntryNode

def main():
    def display_message():
        clear_console()
        print("Welcome to ReceiptChecker!")
        print("Please choose a number on what you want to do:\n1 = Create a receipt list (from file)\n2 = Create a receipt list (manually)\n3 = Exit")
    
    display_message()
    
    print("\nEnter option:")

    while True:
        try:
            choosen_option = int(input(">>> "))

            if choosen_option == 1:
                clear_console()
                print("(Type \"CANCEL\" to go back)\n\nEnter the filename including its extension (e.g., data.txt):")
                while True:
                    file = str(input(">>> "))
                    if file != "CANCEL":
                        try:
                            with open(file, "r") as file:
                                receipt_obj = build_list_from_file(file)
                                ask_confirmation(receipt_obj)
                                display_message()
                                print("\nEnter option:")
                                break
                        except FileNotFoundError:
                            print(f"\nERROR: {file} is not found.")
                    else:
                        display_message()
                        print("\nEnter option:")
                        break
            elif choosen_option == 2:
                receipt_obj = ReceiptEntryList()
                ask_confirmation(receipt_obj)
                display_message()
                print("\nEnter option:")
            elif choosen_option == 3:
                input("\nPress Enter to exit...")
                break
            else:
                print("\nInvalid option. Please enter a number between 1 and 3.")
        except ValueError:
            print("\nInvalid value. Please enter a correct number.")

def build_list_from_file(file):
    receipt = ReceiptEntryList()

    try:
        contents = file.read()
        ctr = 0
        for value in contents.splitlines():
            splitted_value = value.split()
            check_line_length(ctr, splitted_value, value)

            if ctr == 0:
                check_header_line(ctr, splitted_value, value)
                receipt.receipt_number = splitted_value[0]
                receipt.date = splitted_value[1]
                receipt.time = splitted_value[2]
            else:
                check_receipt_entry(ctr, splitted_value, value)
                new_node = ReceiptEntryNode(splitted_value[0], splitted_value[1], float(splitted_value[2]), ctr)

                if receipt.head is None:
                    receipt.head = new_node
                    receipt.tail = new_node
                else:
                    receipt.tail.next_node = new_node
                    new_node.previous_node = receipt.tail
                    receipt.tail = new_node
            ctr += 1
    except FileNotFoundError:
        print("ERROR: INPUT.txt was not found in the working directory of this script file. Please ensure that the file exists and has the correct filename and file extension.")
        exit(0)

    return receipt

def create_list_from_user():
    clear_console()
    receipt = ReceiptEntryList()

    ctr = 1
    while True:
        print("Entry #", ctr, sep="")
        print("\nEnter item name without spaces: ")
        while True:
            item_name = str(input(">>> "))
            if re.search(r"\s", item_name):
                (print("\nINVALID: Please ensure item name has no spaces."))
            else:
                break
        
        print("\nEnter quantity:")
        while True:
            quantity = str(input(">>> "))
            if re.search(r"^[0-9]+$", quantity):
                break
            else:
                print("\nERROR: Invalid quantity. Quantity must be a positive integer (1 and above).")
        
        print("\nEnter unit price: ")
        while True:
            unit_price = str(input(">>> "))
            if re.search(r"^(?:\d+)?(?:\.\d+)?$", unit_price):
                break
            else:
                print("\nERROR: Invalid unit price. Please ensure that it is in correct format (e.g., 150, 250.46, 100.00)")

        new_node = ReceiptEntryNode(item_name, quantity, float(unit_price), ctr)

        if receipt.head is None:
            receipt.head = new_node
            receipt.tail = new_node
        else:
            receipt.tail.next_node = new_node
            new_node.previous_node = receipt.tail
            receipt.tail = new_node

        display_entries(receipt)

        print("\nAdd more entry?\n1 = Yes\n2 = No\n\nEnter option: ")
        
        while True:
            try:
                option = int(input(">>> "))
                if option == 1:
                    clear_console()
                    display_entries(receipt)
                    print()
                    break
                elif option == 2:
                    ask_confirmation(receipt)
                else:
                    clear_console()
                    display_entries(receipt)
                    print("\nAdd more entry?\n1 = Yes\n2 = No")
                    print("\nERROR: Invalid option. Please enter a number between 1 and 2.")
            except ValueError:
                clear_console()
                display_entries(receipt)
                print("\nAdd more entry?\n1 = Yes\n2 = No")
                print("\nERROR: Invalid value. Please enter a correct number.")

        ctr += 1

def check_line_length(ctr, splitted_value, value):
    if len(splitted_value) >= 4:
        if ctr == 0:
            print("ERROR: Multiple values found in the header line of text file. Please ensure that receipt number, date, and, time are the only values at the header line. Receipt registration will be cancelled.")
        else:
            print(f"ERROR: Multiple values found in the receipt entry placed at Line #{ctr + 1} ({value}) of text file. Please ensure that each line of receipt entry contains only the item name, quantity, and unit price. Receipt registration will be cancelled.")
        exit(0)
    elif len(splitted_value) <= 2:
        if ctr == 0:
            print("ERROR: Header line lacks at least one required values (i.e., receipt number, date, or, time). Receipt registration will be cancelled.")
            exit(0)
        else:
            if len(splitted_value) == 0:
                print(f"ERROR: Receipt entry at Line #{(ctr+1)} lacks at least one required values (i.e., item name, quantity, or unit price). Receipt registration will be cancelled.")
            else:
                print(f"ERROR: Receipt entry at Line #{(ctr+1)} ({value}) lacks at least one required values (i.e., item name, quantity, or unit price). Receipt registration will be cancelled.")
            exit(0)

def check_header_line(ctr, splitted_value, value):
    if ctr == 0:
        # Uses RegEx to check if it's a valid receipt number
        filtered_receipt_number = re.search(r"^[\w-]+$", splitted_value[0])
        if filtered_receipt_number is None:
            print("ERROR: Invalid receipt number. Ensure that the receipt number is in correct format (i.e., x-xx-xxxx-xx, where x is a positive whole number). Receipt registration will be cancelled.")
            exit(0)
        
        # Uses datetime module to check if date is valid or not
        try:
            filtered_time = re.search(r"^([0-1][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$", splitted_value[2])
            if filtered_time is None:
                print("ERROR: Invalid date/time. The date and time is set in the future. Receipt registration will be cancelled.")
                exit(0)

            filtered_date = datetime.strptime(splitted_value[1] + " " + splitted_value[2], "%Y/%m/%d %H:%M:%S")
            current_date = datetime.now()

            if filtered_date > current_date:
                print("ERROR: Invalid date/time. The date and time is set in the future. Receipt registration will be cancelled.")
                exit(0)
        except ValueError:
            print("ERROR: Invalid date/time. Either date is not in proper MM/DD/YYYY format or time is not in HH:mm:SS format. Receipt registration will be cancelled.")
            exit(0)

def check_receipt_entry(ctr, splitted_value, value):
    filtered_item_name = re.search(r"^(\w+(_)?){1,}$", splitted_value[0])
    if filtered_item_name is None:
        print(f"ERROR: Invalid item name at Line #{(ctr + 1)} (>>>{splitted_value[0]}<<<, {splitted_value[1]}, {splitted_value[2]}). Item name must only include letters and numbers and can only be separated by underscore.")
        exit()
    
    splitted_item_name = splitted_value[0].split("_")
    splitted_value[0] = '_'.join(word.capitalize() for word in splitted_item_name)

    filtered_quantity = re.search(r"^[0-9]+$", splitted_value[1])
    if filtered_quantity is None:
        print(f"ERROR: Invalid quantity at Line #{(ctr + 1)} ({splitted_value[0]}, >>>{splitted_value[1]}<<<, {splitted_value[2]}). Quantity must be a positive integer (1 or above).")
        exit()
    
    filtered_unit_price = re.search(r"^(?:\d+)?(?:\.\d+)?$", splitted_value[2])
    if filtered_unit_price is None:
        print(f"ERROR: Invalid unit price at Line #{(ctr + 1)} ({splitted_value[0]}, {splitted_value[1]}, >>>{splitted_value[2]}<<<). Ensure that it is in correct format (e.g., 150, 250.46, 100.00)")
        exit()

def ask_confirmation(receipt_obj):
    def display_menu():
        display_entries(receipt_obj)
        print("\nChoose option:\n0 = Go back\n1 = Add entry\n2 = Delete entry\n3 = Edit entry details\n4 = Sort the list by total price in descending order\n5 = Change receipt header\n6 = Export as .TXT file (for formatted results)\n7 = Export as .JSON file (for importing)\n8 = Discard and exit the program.")

    display_menu()
    print("\nEnter option:")

    while True:
        try:
            choosen_option = int(input(">>> "))

            if choosen_option == 0:
                return
            elif choosen_option == 1:
                receipt_obj.add_entry()
                display_entries(receipt_obj)
                display_menu()
                print("\nEnter option:")
            elif choosen_option == 2:
                receipt_obj.delete_entry()
                display_entries(receipt_obj)
                display_menu()
                print("\nEnter option:")
            elif choosen_option == 3:
                receipt_obj.edit_entry_details()
                display_entries(receipt_obj)
                display_menu()
                print("\nEnter option:")
            elif choosen_option == 4:
                receipt_obj.sort_list()
                display_entries(receipt_obj)
                display_menu()
                print("\nEnter option:")
            elif choosen_option == 5:
                clear_console()
                receipt_obj.change_receipt_header()
                display_entries(receipt_obj)
                display_menu()
                print("\nEnter option:")
            elif choosen_option == 6:
                write_receipt_output_file(receipt_obj)
                display_entries(receipt_obj)
                display_menu()
                print("\nEnter option:")
            elif choosen_option == 7:
                receipt_obj.export_as_json()
                display_entries(receipt_obj)
                display_menu()
                print("\nEnter option:")
            elif choosen_option == 8:
                print("The program will now exit.")
                input("\nPress Enter to exit...")
                exit(0)
            else:
                print("\nInvalid option. Please enter a number between 1 and 4.")
        except ValueError:
            print("\nInvalid value. Please enter a correct number.")

def display_entries(receipt_obj):
    clear_console()
    
    spacing_values = get_spacing_values_length(receipt_obj)

    total_price = 0.0
    total_of_items = 0
    current = receipt_obj.head

    print("-" * spacing_values[5])
    if not current:
        print("LIST IS CURRENTLY EMPTY.\nReceipt entries will be previewed here.")
    else:
        date = receipt_obj.date if receipt_obj.date else "<N0_RECEIPT_DATE>"
        time = receipt_obj.time if receipt_obj.time else "<NO_RECEIPT_TIME>"
        formatted_receipt_number = receipt_obj.receipt_number if receipt_obj.receipt_number else "<NO_RECEIPT_CODE>"
        print(f"RECEIPT CODE: {formatted_receipt_number}\nDATE & TIME: {date}, {time}\n")

        column_header = ["POS", "ITEM NAME", "QUANTITY", "UNIT PRICE", "TOTAL PRICE"]
        print("{:{}} {:<{}} {:<{}} {:<{}} {:<{}}".format(
            column_header[0], spacing_values[0] + 2,
            column_header[1], spacing_values[1] + 2,
            column_header[2], spacing_values[2] + 2,
            column_header[3], spacing_values[3] + 2,
            column_header[4], spacing_values[4] + 2
        ))

        while current is not None:
            print("{:<{}} {:<{}} {:<{}} {:<{}} {:<{}}".format(
                current.entry.entry_position, spacing_values[0] + 2,
                current.entry.item_name, spacing_values[1] + 2,
                current.entry.quantity, spacing_values[2] + 2,
                current.entry.unit_price, spacing_values[3] + 2,
                current.entry.total_price, spacing_values[4] + 2
            ))

            total_price += current.entry.total_price

            total_price = round_num(total_price)
            total_of_items += 1

            current = current.next_node

        if total_of_items > 1 or total_of_items == 0:
            item_string = "items"
        else:
            item_string = "item"
        print(f"\nTOTAL SUM: {total_price:.2f} ({total_of_items} {item_string})")
    print("-" * spacing_values[5])

def get_spacing_values_length(receipt_obj):
    position_max_length = 2
    item_name_max_length = 9
    quantity_max_length = 8
    unit_price_max_length = 10
    total_price_max_length = 11

    current = receipt_obj.head

    while current is not None:
        item_name_max_length = max(item_name_max_length, len(current.entry.item_name))
        quantity_max_length = max(quantity_max_length, len(current.entry.quantity))
        unit_price_max_length = max(unit_price_max_length, len(str(current.entry.unit_price)))
        total_price_max_length = max(total_price_max_length, len(str(current.entry.total_price)))

        current = current.next_node
    
    spaces_total_length = 10 + position_max_length + item_name_max_length + quantity_max_length + unit_price_max_length + total_price_max_length
    return [position_max_length, item_name_max_length, quantity_max_length, unit_price_max_length, total_price_max_length, spaces_total_length]

def write_receipt_output_file(receipt_obj):
    clear_console()

    if not receipt_obj.head:
        print("Cannot write results as there is nothing to export.")
        input("Press Enter to proceed...")
        return
    
    print("(Type \"CANCEL\" to go back)\n\nEnter the filename w/ \".txt\" in the end:")
    while True:
        output = str(input(">>> "))
        if output == "CANCEL":
            return
        elif not re.search(r"^[\w\-. ]+$", output):
            print("\nInvalid filename. Ensure that no illegal characters are used (i.e., \ / : * ? \" < > |).")
        elif os.path.exists(output):
            print(f"\nFile \"{output}\" already exist. Please use a different filename.")
        else:
            break

    if not os.path.exists("output"):
        os.makedirs("output")
    else:
        pass

    with open("output/" + output, "w") as f:
        current = receipt_obj.head
        spacing_values = get_spacing_values_length(receipt_obj)
        total_price = 0.0
        total_of_items = 0

        f.write("-" * spacing_values[5])
        date = receipt_obj.date if receipt_obj.date else "<N0_RECEIPT_DATE>"
        time = receipt_obj.time if receipt_obj.time else "<NO_RECEIPT_TIME>"
        formatted_receipt_number = receipt_obj.receipt_number if receipt_obj.receipt_number else "<NO_RECEIPT_CODE>"
        f.write(f"\nRECEIPT CODE: {formatted_receipt_number}\nDATE & TIME: {date}, {time}\n")

        column_header = ["POS", "ITEM NAME", "QUANTITY", "UNIT PRICE", "TOTAL PRICE"]
        f.write("\n{:<{}} {:<{}} {:<{}} {:<{}} {:<{}}".format(
                column_header[0], spacing_values[0] + 2,
                column_header[1], spacing_values[1] + 2,
                column_header[2], spacing_values[2] + 2,
                column_header[3], spacing_values[3] + 2,
                column_header[4], spacing_values[4] + 2
        ))
        
        while current is not None:
            f.write("\n{:<{}} {:<{}} {:<{}} {:<{}} {:<{}}".format(
                current.entry.entry_position, spacing_values[0] + 2,
                current.entry.item_name, spacing_values[1] + 2,
                current.entry.quantity, spacing_values[2] + 2,
                current.entry.unit_price, spacing_values[3] + 2,
                current.entry.total_price, spacing_values[4] + 2,
        ))
            total_price += current.entry.total_price

            total_price = round_num(total_price)
            total_of_items += 1

            current = current.next_node
        
        if total_of_items > 1 or total_of_items == 0:
            item_string = "items"
        else:
            item_string = "item"

        f.write(f"\n\nTOTAL SUM: {total_price:.2f} ({total_of_items} {item_string})")
        f.write("\n" + "-" * spacing_values[5])
        f.flush()
        print(f"\nSUCCESS: The results has been saved to \"{output}\"")
        input("Press Enter to proceed...")

def add_entry_quantity(entry_quantity):
    # Since quantities with units are treated 1, they must be filtered here using RegEx
    filtered_quantity = re.search(r"^(?:0*[1-9][0-9]*)?(?:\.\d*|0+\.\d+)?(?:g|mL|L|kg)$", entry_quantity)
    if filtered_quantity:
        return 1
    else:
        return int(entry_quantity)

def round_num(value):
    num = Decimal(str(value))
    rounded_num = num.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return float(rounded_num)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[H", end="")

if __name__ == "__main__":
    main()
