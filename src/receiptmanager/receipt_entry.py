"""Classes for the structure of receipt list and its entries."""
from datetime import datetime
from src.receiptmanager.utils import round_num
from src.receiptmanager.config import load_config

class ReceiptEntry:
    """ Defines the attributes/types that is expected for each one."""
    item_name: str
    quantity: str
    unit_price: float
    total_price: float
    entry_position: int

class ReceiptEntryNode:
    """Defines the structure of an entry in receipt entry list."""
    def __init__(self, item_name, quantity, unit_price, entry_position):
        self.entry = ReceiptEntry()
        self.entry.item_name = item_name
        self.entry.quantity = quantity
        self.entry.unit_price = round_num(unit_price)
        self.entry.total_price = round_num(int(quantity) * self.entry.unit_price)
        self.entry.entry_position = entry_position
        self.previous_node = None
        self.next_node = None

class ReceiptEntryList:
    """Defines the structure of receipt entry list."""
    def __init__(self):
        current_date_and_time = datetime.now()

        self.receipt_code = "RM-" + str(current_date_and_time.strftime("%y%m%d_%H%M%S"))
        self.date = current_date_and_time.strftime("%Y/%m/%d")
        self.time = current_date_and_time.strftime("%H:%M:%S")
        self.head = None
        self.tail = None
        self.config = load_config()
