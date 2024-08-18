import json
import os
from src.receiptmanager.constants import JSON_SAVED_RESULTS_FOLDER_PATH, TXT_SAVED_RESULTS_FOLDER_PATH
from src.receiptmanager.legacy.receipt_validator import check_line_length, check_header_line, check_receipt_entry
from src.receiptmanager.receipt_entry import ReceiptEntryNode, ReceiptEntryList
from src.receiptmanager.utils import is_path_exists

def get_valid_json_file():
    while True:
        file_name = str(input(">>> "))
        if file_name == "CANCEL":
            return
        if is_path_exists(JSON_SAVED_RESULTS_FOLDER_PATH + file_name + ".json"):
            return file_name
        else:
            print(f"\nERROR: {file_name}.json is not found.")

def get_valid_txt_file():
    while True:
        file_name = str(input(">>> "))
        if file_name == "CANCEL":
            return
        if os.path.exists(TXT_SAVED_RESULTS_FOLDER_PATH + file_name + ".txt"):
            return file_name
        else:
            print(f"\nERROR: {file_name}.txt is not found.")

def import_using_json(file):
    receipt_obj = ReceiptEntryList()
    json_file = json.load(file)

    receipt_obj.receipt_code = json_file["receipt_header"]["receipt_code"]
    receipt_obj.date = json_file["receipt_header"]["date"]
    receipt_obj.time = json_file["receipt_header"]["time"]

    for entry in json_file["receipt_entries"]:
        new_node = ReceiptEntryNode(entry["item_name"],
                                    entry["quantity"],
                                    float(entry["unit_price"]),
                                    entry["entry_position"])

        if receipt_obj.head is None:
            receipt_obj.head = new_node
            receipt_obj.tail = new_node
        else:
            receipt_obj.tail.next_node = new_node
            new_node.previous_node = receipt_obj.tail
            receipt_obj.tail = new_node

    return receipt_obj

def import_using_txt(file):
    receipt_obj = ReceiptEntryList()

    try:
        contents = file.read()
        ctr = 0
        for value in contents.splitlines():
            splitted_value = value.split()
            check_line_length(ctr, splitted_value, value)

            if ctr == 0:
                check_header_line(ctr, splitted_value, value)
                receipt_obj.receipt_code = splitted_value[0]
                receipt_obj.date = splitted_value[1]
                receipt_obj.time = splitted_value[2]
            else:
                check_receipt_entry(ctr, splitted_value, value)
                new_node = ReceiptEntryNode(splitted_value[0], splitted_value[1], float(splitted_value[2]), ctr)

                if receipt_obj.head is None:
                    receipt_obj.head = new_node
                    receipt_obj.tail = new_node
                else:
                    receipt_obj.tail.next_node = new_node
                    new_node.previous_node = receipt_obj.tail
                    receipt_obj.tail = new_node
            ctr += 1
    except FileNotFoundError:
        print("ERROR: INPUT.txt was not found in the working directory of this script file. Please ensure that the file exists and has the correct filename and file extension.")
        exit(0)

    return receipt_obj
