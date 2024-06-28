import os
import json
from receiptmanager_vvnzylt.receipt_entry import ReceiptEntryList, ReceiptEntryNode
from receiptmanager_vvnzylt.legacy.receipt_validator import check_line_length, check_header_line, check_receipt_entry

def choose_action(action):
    if action == "IMPORT_USING_JSON":
        json_file = get_valid_json_file()

        if json_file is not None:
            with open("user_data/saved_results/json/" + json_file + ".json", "r", encoding="utf-8") as file:
                receipt_obj = import_using_json(file)
                receipt_options_menu(receipt_obj)
        return
    elif action == "IMPORT_USING_TXT":
        txt_file = get_valid_txt_file()

        if txt_file is not None:
            with open("user_data/saved_results/txt/" + txt_file + ".txt", "r", encoding="utf-8") as file:
                receipt_obj = import_using_txt(file)
                receipt_options_menu(receipt_obj)
        return
    elif action == "CREATE_MANUALLY":
        receipt_obj = ReceiptEntryList()
        receipt_options_menu(receipt_obj)
        return

def get_valid_json_file():
    print("(Type \"CANCEL\" to go back)\n\nEnter file name:")
    while True:
        file_name = str(input(">>> "))
        if file_name == "CANCEL":
            return
        if os.path.exists("user_data/saved_results/json/" + file_name + ".json"):
            return file_name
        else:
            print(f"\nERROR: {file_name}.json is not found.")

def get_valid_txt_file():
    print("(Type \"CANCEL\" to go back)\n\nEnter file name:")
    while True:
        file_name = str(input(">>> "))
        if file_name == "CANCEL":
            return
        if os.path.exists("user_data/saved_results/txt/" + file_name + ".txt"):
            return file_name
        else:
            print(f"\nERROR: {file_name}.txt is not found.")

def import_using_json(file):
    receipt_obj = ReceiptEntryList()

    json_file = json.load(file)

    receipt_obj.receipt_number = json_file["receipt_header"]["receipt_code"]
    receipt_obj.date = json_file["receipt_header"]["date"]
    receipt_obj.time = json_file["receipt_header"]["time"]

    for x in range(len(json_file["entries"])):
        new_node = ReceiptEntryNode(json_file["entries"][x]["item_name"], json_file["entries"][x]["quantity"], float(json_file["entries"][x]["unit_price"]), json_file["entries"][x]["entry_position"])

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
                receipt_obj.receipt_number = splitted_value[0]
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

def receipt_options_menu(receipt_obj):
    def display_menu():
        receipt_obj.display_entries()
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
            elif choosen_option == 2:
                receipt_obj.delete_entry()
            elif choosen_option == 3:
                receipt_obj.edit_entry_details()
            elif choosen_option == 4:
                receipt_obj.sort_list()
            elif choosen_option == 5:
                receipt_obj.change_receipt_header()
            elif choosen_option == 6:
                receipt_obj.export_as_txt()
            elif choosen_option == 7:
                receipt_obj.export_as_json()
                print("\nEnter option:")
            elif choosen_option == 8:
                print("The program will now exit.")
                input("\nPress Enter to exit...")
                exit(0)
            else:
                print("\nInvalid option. Please enter a number between 1 and 4.")
                continue
        except ValueError:
            print("\nInvalid value. Please enter a correct number.")
            continue

        display_menu()
        print("\nEnter option:")
