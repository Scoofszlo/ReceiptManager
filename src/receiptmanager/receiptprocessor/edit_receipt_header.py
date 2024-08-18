from datetime import datetime
import re
from src.receiptmanager.utils import clear_console

def display_receipt_header(receipt_obj):
    clear_console()
    print(f"\nReceipt code: {receipt_obj.receipt_code}")
    print(f"Date/time: {receipt_obj.date}, {receipt_obj.time}")
    print("\nChoose option:\n0 = Go back\n1 = Change receipt code\n2 = Change date\n3 = Change time")

def get_new_receipt_code_input():
    while True:
        new_receipt_code = str(input(">>> "))
        if re.search(r"^\s*$", new_receipt_code):
            print("\nERROR: Invalid receipt code as there are no characters entered.")
            continue
        return new_receipt_code
    
def get_new_date_input():
    while True:
        new_date = str(input(">>> "))
        if re.search(r"^\s*$", new_date):
            print("\nERROR: Invalid date as there are no characters entered.")
            continue
        elif new_date == "CANCEL":
            return new_date
        elif is_invalid_date_format(new_date):
            print("\nERROR: Invalid date. Please ensure that date is in proper format YYYY/MM/DD format (e.g., 2024/05/20)")
            continue
        return datetime.strptime(new_date, "%Y/%m/%d")
    
def get_new_time_input():
    """
    Gets user input for new time to be changed. The user input will loop
    forever whenever user enters an empty string or whitespace characters, or if
    user enters other than a valid 24-hour time format value. In the end, this
    functions returns either a time with seconds with or without seconds included.
    """
    while True:
        new_time = str(input(">>> "))
        if re.search(r"^\s*$", new_time):
            print("\nERROR: Invalid time as there are no characters entered.")
            continue
        elif new_time == "CANCEL":
            return new_time
        elif is_invalid_time_format(new_time):
            print("\nERROR: Invalid time. Please ensure that time is in proper HH:MM:SS format (e.g., 20:01:59)")
            continue
        try:
            return datetime.strptime(new_time, "%H:%M:%S")
        except ValueError:
            return datetime.strptime(new_time, "%H:%M")

def is_invalid_date_format(new_date):
    try:
        datetime.strptime(new_date, "%Y/%m/%d")
        return False
    except ValueError:
        return True

def is_invalid_time_format(new_time):
    """
    Checks whether the entered time is a valid 24-hour format or not.
    There are two passes to validate the input. The first pass checks 
    if seconds are included. If that fails, it goes through the second
    pass wherein seconds ae not required to be included.
    However, hours and minutes are still required.
    """
    try:
        datetime.strptime(new_time, "%H:%M:%S")
    except ValueError:
        try:
            datetime.strptime(new_time, "%H:%M")
            return False
        except ValueError:
            return True

def parse_current_receipt_date(receipt_obj):
    return datetime.strptime(receipt_obj.date, "%Y/%m/%d") if receipt_obj.date else None

def parse_current_receipt_time(receipt_obj):
    return datetime.strptime(receipt_obj.time, "%H:%M:%S") if receipt_obj.time else None

def format_date(date):
    return date.strftime("%Y/%m/%d")

def format_time(time):
    return time.strftime("%H:%M:%S")

def change_receipt_code(receipt_obj, new_receipt_code):
    receipt_obj.receipt_code = new_receipt_code

def change_receipt_date(receipt_obj, new_date):
    receipt_obj.date = str(new_date.strftime("%Y/%m/%d"))

def change_receipt_time(receipt_obj, new_time):
    receipt_obj.time = str(new_time.strftime("%H:%M:%S"))
