import re
from src.receiptmanager.receipt_entry import ReceiptEntryNode

def get_new_entry_idx_pos(receipt_obj):
    idx_pos = receipt_obj.tail.entry.entry_position + 1 if receipt_obj.tail else 1
    return idx_pos

def get_item_name():
    while True:
        item_name = str(input(">>> "))
        if item_name == "DONE":
            return None
        else:
            return item_name

def get_quantity():
    while True:
        quantity = str(input(">>> "))
        if quantity == "DONE":
            return None
        if re.search(r"^[0-9]+$", quantity):
            return quantity
        else:
            print("\nERROR: Invalid quantity. Quantity must be a positive integer (1 and above).")

def get_unit_price():
    while True:
        unit_price = str(input(">>> "))
        if unit_price == "DONE":
            return None
        if re.search(r"^(?:\d+)?(?:\.\d+)?$", unit_price):
            return unit_price
        else:
            print("\nERROR: Invalid unit price. Please ensure that it is in correct format (e.g., 150, 250.46, 100.00)")

def add_entry(receipt_obj, item_name, quantity, unit_price, ctr):
    new_node = ReceiptEntryNode(item_name, quantity, float(unit_price), ctr)

    # If there is no entry existing in receipt_obj, the new node will be appended. Otherwise, it will be appended next to the last node
    if receipt_obj.head is None:
        receipt_obj.head = new_node
        receipt_obj.tail = new_node
    else:
        receipt_obj.tail.next_node = new_node
        new_node.previous_node = receipt_obj.tail
        receipt_obj.tail = new_node
