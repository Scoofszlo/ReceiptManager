import json
import re
import os
from src.receiptmanager.constants import TXT_SAVED_RESULTS_FOLDER_PATH, JSON_SAVED_RESULTS_FOLDER_PATH
from src.receiptmanager.receiptprocessor.general import get_spacing_values_length, get_currency_symbol
from src.receiptmanager.utils import round_num

def get_file_name_input(receipt_obj):
    while True:
        file_name = str(input(">>> "))

        if re.search(r"^\s+$", file_name):
            file_name = receipt_obj.receipt_code

        if file_name == "CANCEL":
            return file_name
        elif not re.search(r"^[\w\-.]+$", file_name):
            print("\nERROR: Invalid file name. Ensure that no illegal characters are used (i.e., \\ / : * ? \" < > |).")
            continue
        elif os.path.exists("program_data/saved_results/txt/" + file_name + ".txt"):
            print(f"\nFile \"{file_name}\" already exist. Please use a different file name.")
            continue
        return file_name

def export_as_txt(receipt_obj, file_name):
    """
    Writes to a file specified by the user in a TXT format. 
    """
    with open(TXT_SAVED_RESULTS_FOLDER_PATH + file_name + ".txt", "w", encoding="utf-8") as f:
        spacing_values = get_spacing_values_length(receipt_obj)
        total_price = 0.0
        total_of_items = 0

        __write_border(f, spacing_values)
        __write_receipt_header(f, receipt_obj, spacing_values)
        __write_receipt_entries(f, receipt_obj, spacing_values, total_price, total_of_items)
        __write_receipt_summary(f, receipt_obj, total_price, total_of_items)
        __write_border(f, spacing_values)

        f.flush()
        print(f"\nSUCCESS: The results has been saved to \"program_data/saved_results/txt/{file_name}.txt\"")
        input("Press Enter to proceed...")

def export_as_json(receipt_obj, file_name):
    """Exports the receipt list in JSON format."""

    receipt = {}
    receipt_header = __get_receipt_header_details(receipt_obj)
    receipt_entries = __get_receipt_entries(receipt_obj)

    # Adds the receipt_header and receipt_entries to the receipt
    receipt["receipt_header"] = receipt_header
    receipt["receipt_entries"] = receipt_entries

    # Convert the receipt object to a JSON-formatted string with 4-space
    # indentation and non-ASCII characters preserved
    json_file = json.dumps(receipt, indent=4, ensure_ascii=False)
    with open(JSON_SAVED_RESULTS_FOLDER_PATH + file_name + ".json", "w", encoding="utf-8") as f:
        f.write(json_file)
        f.flush()
        print(f"\nSUCCESS: The results has been saved to \"{JSON_SAVED_RESULTS_FOLDER_PATH}{file_name}.json\"")
        input("Press Enter to proceed...")

def __get_receipt_header_details(receipt_obj):
    """
    Retrieves all the receipt metadata from receipt_obj and organized them
    in a dictionary form. Finally, the dictionary is then returned.
    """
    receipt_header = {
        "receipt_code": receipt_obj.receipt_code,
        "date": receipt_obj.date,
        "time": receipt_obj.time
    }

    return receipt_header

def __get_receipt_entries(receipt_obj):
    """
    This access the data of receipt_obj through it's head or basically the first
    item of it. And then we traverse toreceipt_obj using looping to retrieve all
    the entries and add them to the list. After that, the list will be returned.
    """

    receipt_entries = []
    current = receipt_obj.head

    while current:
        entry = {
            "entry_position": current.entry.entry_position,
            "item_name": current.entry.item_name,
            "quantity": current.entry.quantity,
            "unit_price": current.entry.unit_price,
            "total_price": current.entry.total_price
        }
        receipt_entries.append(entry)
        current = current.next_node
    
    return receipt_entries

def __write_border(f, spacing_values):
    f.write("-" * spacing_values[5])

def __write_receipt_header(f, receipt_obj, spacing_values):
    date = receipt_obj.date if receipt_obj.date else "<N0_RECEIPT_DATE>"
    time = receipt_obj.time if receipt_obj.time else "<NO_RECEIPT_TIME>"
    receipt_code = receipt_obj.receipt_code if receipt_obj.receipt_code else "<NO_RECEIPT_CODE>"

    f.write("\n{:^{}}".format(
        "RECEIPT CODE: " + receipt_code, spacing_values[5]
    ))

    f.write("\n{:^{}}".format(
        "DATE & TIME: " + date + ", " + time, spacing_values[5]
    ))

def __write_receipt_entries(f, receipt_obj, spacing_values, total_price, total_of_items):
    current = receipt_obj.head

    column_header = ["POS", "ITEM NAME", "QUANTITY", "UNIT PRICE", "TOTAL PRICE"]
    f.write("\n\n{:<{}} {:>{}} {:>{}} {:>{}} {:>{}}".format(
            column_header[0], spacing_values[0] + 2,
            column_header[1], spacing_values[1] + 2,
            column_header[2], spacing_values[2] + 2,
            column_header[3], spacing_values[3] + 2,
            column_header[4], spacing_values[4] + 2
    ))

    while current is not None:
        currency = get_currency_symbol(receipt_obj.config)
        formatted_quantity = f"{int(current.entry.quantity):,}"
        formatted_unit_price = f"{currency}{float(current.entry.unit_price):,.2f}" if currency else f"{float(current.entry.unit_price):,.2f}"
        formatted_total_price = f"{currency}{float(current.entry.total_price):,.2f}" if currency else f"{float(current.entry.total_price):,.2f}"
        f.write("\n{:<{}} {:>{}} {:>{}} {:>{}} {:>{}}".format(
            current.entry.entry_position, spacing_values[0] + 2,
            current.entry.item_name, spacing_values[1] + 2,
            formatted_quantity, spacing_values[2] + 2,
            formatted_unit_price, spacing_values[3] + 2,
            formatted_total_price, spacing_values[4] + 2,
    ))
        total_price += current.entry.total_price

        total_price = round_num(total_price)
        total_of_items += 1

        current = current.next_node

def __write_receipt_summary(f, receipt_obj, total_price, total_of_items):
    if total_of_items > 1 or total_of_items == 0:
        item_string = "items"
    else:
        item_string = "item"

    if get_currency_symbol(receipt_obj.config):
        f.write(f"\n\nTOTAL SUM: {get_currency_symbol(receipt_obj.config)}{total_price:,.2f} ({total_of_items} {item_string})")
    else:
        f.write(f"\n\nTOTAL SUM: {total_price:,.2f} ({total_of_items} {item_string})")

    f.write("\n")
