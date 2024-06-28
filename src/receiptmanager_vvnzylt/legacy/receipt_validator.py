import re
from datetime import datetime

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
