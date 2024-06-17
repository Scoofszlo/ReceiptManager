import re
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

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
        self.entry.unit_price = self.round_num(unit_price)
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
    
    def round_num(self, value):
        num = Decimal(str(value))
        rounded_num = num.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        print(rounded_num)
        return float(rounded_num)

class ReceiptEntryList:
    # This function is always called when this class is instantiated.
    # Several variables are declared here as they are crucial for other
    # functions to work for this class
    def __init__(self):
        self.receipt_number = None
        self.date = None
        self.time = None
        self.head = None
        self.tail = None

    def build_list_from_file(self):
        try:
            # Reads the file from INPUT.txt
            with open("sample_input.txt", "r") as file:
                contents = file.read()
                ctr = 0
                for value in contents.splitlines():
                    splitted_value = value.split()
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
                    else:
                        # This if condition ensures the header line will not be included as a receipt entry from INPUT.txt
                        if ctr == 0:
                            # Uses RegEx to check if it's a valid receipt number
                            filtered_receipt_number = re.search(r"^\d{1}-\d{2}-\d{4}-\d{2}$", splitted_value[0])
                            if filtered_receipt_number is None:
                                print("ERROR: Invalid receipt number. Ensure that the receipt number is in correct format (i.e., x-xx-xxxx-xx, where x is a positive whole number). Receipt registration will be cancelled.")
                                exit(0)
                            
                            # Uses datetime module to check if date is valid or not
                            try:
                                filtered_time = re.search(r"^([0-1][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$", splitted_value[2])
                                if filtered_time is None:
                                    print("ERROR: Invalid date/time. The date and time is set in the future. Receipt registration will be cancelled.")
                                    exit(0)

                                filtered_date = datetime.strptime(splitted_value[1] + " " + splitted_value[2], "%m/%d/%Y %H:%M:%S")
                                current_date = datetime.now()

                                if filtered_date > current_date:
                                    print("ERROR: Invalid date/time. The date and time is set in the future. Receipt registration will be cancelled.")
                                    exit(0)
                            except ValueError:
                                print("ERROR: Invalid date/time. Either date is not in proper MM/DD/YYYY format or time is not in HH:mm:SS format. Receipt registration will be cancelled.")
                                exit(0)
                            
                            # When no error happens or if the values are all valid, they will now be registered as a valid header line
                            self.receipt_number = splitted_value[0]
                            self.date = splitted_value[1]
                            self.time = splitted_value[2]
                        else:
                            # Checks whether the item name of the receipt is a valid value or not
                            filtered_item_name = re.search(r"^(\w+(_)?){1,}$", splitted_value[0])
                            if filtered_item_name is None:
                                print(f"ERROR: Invalid item name at Line #{(ctr + 1)} (>>>{splitted_value[0]}<<<, {splitted_value[1]}, {splitted_value[2]}). Item name must only include letters and numbers and can only be separated by underscore.")
                                exit()
                            
                            # Turns item name into pascal case. Take note that using title() can be an alternative for this one
                            # but sometimes it doesn't work in some situations
                            splitted_item_name = splitted_value[0].split("_")
                            splitted_value[0] = '_'.join(word.capitalize() for word in splitted_item_name)

                            # Checks the item quantity whether if it is a positive integer or a quantity combined with valid units
                            filtered_quantity = re.search(r"^(?!0+(?:\.0+)?(?:g|kg|mL|L)?$)([1-9]\d*|0)(\.\d+(g|kg|mL|L))?(g|kg|mL|L)?$", splitted_value[1])
                            if filtered_quantity is None:
                                print(f"ERROR: Invalid quantity at Line #{(ctr + 1)} ({splitted_value[0]}, >>>{splitted_value[1]}<<<, {splitted_value[2]}). Quantity must be a positive integer (1 and above) or a combination of positive integer/floating number and a unit (i.e., g, kg, mL, or L).")
                                exit()
                            
                            # Checks the item unit price starts with "P" and has succeeding integer or float number
                            filtered_unit_price = re.search(r"^P(?:\d+)?(?:\.\d+)?$", splitted_value[2])
                            if filtered_unit_price is None:
                                print(f"ERROR: Invalid unit price at Line #{(ctr + 1)} ({splitted_value[0]}, {splitted_value[1]}, >>>{splitted_value[2]}<<<). Ensure that it is in correct format (e.g., P250.46, P100.00)")
                                exit()
                        
                            # When no error happens or if the values are all valid, this receipt entry will be registered in a node.
                            # 3rd argument contains float() to ensure that the data being passed is a float. "1:" means the letter P in unit price will not be included for passing the value.
                            new_node = ReceiptEntryNode(splitted_value[0], splitted_value[1], float(splitted_value[2][1:]))

                            if self.head is None:
                                self.head = new_node
                                self.tail = new_node
                            else:
                                self.tail.next_node = new_node
                                new_node.previous_node = self.tail
                                self.tail = new_node
                        ctr += 1
        except FileNotFoundError:
            print("ERROR: INPUT.txt was not found in the working directory of this script file. Please ensure that the file exists and has the correct filename and file extension.")
            exit(0)

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
    
    def write_receipt_output_file(self):
        f = open("sample_output.txt", "w")

        # Parses the time and date stored from header line using datetime module
        date = datetime.strptime(self.date, "%m/%d/%Y")
        time = datetime.strptime(self.time, "%H:%M:%S")

        formatted_date = date.strftime("%Y/%m/%d")
        formatted_time = time.strftime("%I:%M:%S %p")

        # Writes the rceipt number, along with formatted date and time in the OUTPUT.txt header line
        f.write(f"{self.receipt_number} {formatted_date} {formatted_time}\n")

        current = self.head
        total_price = 0.0
        total_of_items = 0

        while current is not None:
            f.write(f"{current.entry.item_name} {current.entry.quantity} P{current.entry.unit_price:.2f} P{current.entry.total_price:.2f}\n")
            total_price += current.entry.total_price

            # Ensures that the displayed total value will not result in weird x.xx000001 value when it should be x.xx
            total_price = round(total_price, 2)

            # Since quantities with units are treated 1, they must be filtered here using RegEx
            filtered_quantity = re.search(r"^(?:0*[1-9][0-9]*)?(?:\.\d*|0+\.\d+)?(?:g|mL|L|kg)$", current.entry.quantity)
            if filtered_quantity:
                total_of_items += 1
            else:
                total_of_items += int(current.entry.quantity)
                
            current = current.next_node
        
        if total_of_items > 1 or total_of_items == 0:
            item_string = "items"
        else:
            item_string = "item"
        f.write(f"P{total_price:.2f} {total_of_items}_{item_string}")
        print(f"SUCCESS: Registration of Receipt # {self.receipt_number} to OUTPUT.txt was successful. There are {total_of_items} {item_string} registered, amouting to a total of P{total_price} overall.")
        f.close()
