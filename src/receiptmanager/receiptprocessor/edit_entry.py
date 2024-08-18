import re
from src.receiptmanager.utils import clear_console, round_num

def display_entry_details(node):
    clear_console()
    print(f"POS: {node.entry.entry_position}\nITEM NAME: {node.entry.item_name}\nQUANTITY: {node.entry.quantity}\nUNIT PRICE: {node.entry.unit_price}")

def get_entry_to_edit(position, receipt_obj):
    current = receipt_obj.head
    while current:
        if position == current.entry.entry_position:
            return current
        current = current.next_node

def get_new_item_name_input():
    while True:
        new_name = str(input(">>> "))
        if re.search(r"^\s*$", new_name):
            print("\nERROR: Invalid name as there are no characters entered.")
            continue
        return new_name

def get_new_quantity_input():
    while True:
        new_quantity = str(input(">>> "))
        if re.search(r"^[0-9]+$", new_quantity):
            return new_quantity
        else:
            print("\nERROR: Invalid quantity. Quantity must be a positive integer (1 and above).")

def get_new_unit_price_input():
    while True:
        new_unit_price = str(input(">>> "))
        if re.search(r"^(?:\d+)?(?:\.\d+)?$", new_unit_price):
            return new_unit_price
        else:
            print("\nERROR: Invalid unit price. Please ensure that it is in correct format (e.g., 150, 250.46, 100.00)")

def change_entry_name(node, new_name):
    node.entry.item_name = new_name

def change_entry_quantity(node, new_quantity):
    node.entry.quantity = new_quantity

def change_entry_unit_price(node, new_unit_price):
    node.entry.unit_price = float(new_unit_price)

def change_entry_total_price(node, new_value, action):
    if action == "CHANGE_QUANTITY":
        node.entry.total_price = round_num(int(new_value) * float(node.entry.unit_price))
    if action == "CHANGE_UNIT_PRICE":
        node.entry.total_price = round_num(int(node.entry.quantity) * float(new_value))
