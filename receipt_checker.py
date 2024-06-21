import re
from decimal import Decimal, ROUND_HALF_UP

def round_num(value):
    num = Decimal(str(value))
    rounded_num = num.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return float(rounded_num)

class ReceiptEntry:
    item_name: str
    quantity: str
    unit_price: float
    total_price: float

class ReceiptEntryNode:
    def __init__(self, item_name, quantity, unit_price):
        self.entry = ReceiptEntry()
        self.entry.item_name = item_name
        self.entry.quantity = quantity
        self.entry.unit_price = round_num(unit_price)
        self.entry.total_price = self.compute_total_price(quantity, self.entry.unit_price)
        self.previous_node = None
        self.next_node = None

    def compute_total_price(self, quantity, unit_price):
        # Since quantities with units are treated 1, they must be checked using RegEx 
        filtered_quantity = re.search(r"^(?!0+(?:\.0+)?(?:g|kg|mL|L)?$)([1-9]\d*)?(([1-9]\d*|0)\.\d+)?(g|kg|mL|L)$", quantity)
        if filtered_quantity:
            quantity = 1
        else:
            pass
        # Returns a computed total_price value to the self.entry.total_price above at the ReceiptEntryNode constructor
        return int(quantity) * unit_price

class ReceiptEntryList:
    def __init__(self):
        self.receipt_number = None
        self.date = None
        self.time = None
        self.head = None
        self.tail = None

    def swap(self, node_1, node_2):
        node_1.item_name, node_2.item_name = node_2.item_name, node_1.item_name
        node_1.quantity, node_2.quantity = node_2.quantity, node_1.quantity
        node_1.unit_price, node_2.unit_price = node_2.unit_price, node_1.unit_price
        node_1.total_price, node_2.total_price = node_2.total_price, node_1.total_price

    def sort_list(self):
        current = self.head

        while current is not None:
            next_value = current.next_node
            while next_value is not None:
                # Swapping will happen if the current node has less value than its next node. However, if there are items that have same values,
                # string comparison will happen in which letters will be arranged from Z to A.
                if (current.entry.total_price < next_value.entry.total_price) or (current.entry.total_price == next_value.entry.total_price and current.entry.item_name < next_value.entry.item_name):
                    self.swap(current.entry, next_value.entry)
                next_value = next_value.next_node
            current = current.next_node
