def sort_by_item_name(receipt_obj):
    current = receipt_obj.head

    while current is not None:
        next_value = current.next_node
        while next_value is not None:
            if current.entry.item_name > next_value.entry.item_name:
                __swap(current.entry, next_value.entry)
            next_value = next_value.next_node
        current = current.next_node

    __display_success_message()
    

def sort_by_quantity(receipt_obj):
    current = receipt_obj.head

    while current is not None:
        next_value = current.next_node
        while next_value is not None:
            if int(current.entry.quantity) > int(next_value.entry.quantity):
                __swap(current.entry, next_value.entry)
            next_value = next_value.next_node
        current = current.next_node

    __display_success_message()

def sort_by_unit_price(receipt_obj):
    current = receipt_obj.head

    while current is not None:
        next_value = current.next_node
        while next_value is not None:
            if float(current.entry.unit_price) > float(next_value.entry.unit_price):
                __swap(current.entry, next_value.entry)
            next_value = next_value.next_node
        current = current.next_node

    __display_success_message()

def sort_by_total_price(receipt_obj):
    current = receipt_obj.head

    while current is not None:
        next_value = current.next_node
        while next_value is not None:
            # Swapping will happen if the current node has less value than its next node. However, if there are items that have same values,
            # string comparison will happen in which letters will be arranged from Z to A.
            if (current.entry.total_price < next_value.entry.total_price) or (current.entry.total_price == next_value.entry.total_price and current.entry.item_name < next_value.entry.item_name):
                __swap(current.entry, next_value.entry)
            next_value = next_value.next_node
        current = current.next_node

    __display_success_message()
    
def __swap(node_1, node_2):
    node_1.item_name, node_2.item_name = node_2.item_name, node_1.item_name
    node_1.quantity, node_2.quantity = node_2.quantity, node_1.quantity
    node_1.unit_price, node_2.unit_price = node_2.unit_price, node_1.unit_price
    node_1.total_price, node_2.total_price = node_2.total_price, node_1.total_price

def __display_success_message():
    print("\nSUCCESS: Receipt entries sorted successfully.")
    input("Press Enter to proceed.")
