import re
import os
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

def round_num(value):
    num = Decimal(str(value))
    rounded_num = num.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return float(rounded_num)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[H", end="")

class ReceiptEntry:
    item_name: str
    quantity: str
    unit_price: float
    total_price: float
    entry_position: int

class ReceiptEntryNode:
    def __init__(self, item_name, quantity, unit_price, entry_position):
        self.entry = ReceiptEntry()
        self.entry.item_name = item_name
        self.entry.quantity = quantity
        self.entry.unit_price = round_num(unit_price)
        self.entry.total_price = self.compute_total_price(quantity, self.entry.unit_price)
        self.entry.entry_position = entry_position
        self.previous_node = None
        self.next_node = None

    def compute_total_price(self, quantity, unit_price):
        return int(quantity) * unit_price

class ReceiptEntryList:
    def __init__(self):
        self.receipt_number = None
        self.date = None
        self.time = None
        self.head = None
        self.tail = None

    def add_entry(self):
        clear_console()

        while True:
            print("(Type \"CANCEL\" to go back)\n")
            ctr = self.tail.entry.entry_position + 1 if self.tail else 1
            print("Entry #", ctr, sep="")
            print("Enter item name without spaces: ")
            while True:
                item_name = str(input(">>> "))
                if item_name == "CANCEL":
                    return
                if re.search(r"\s", item_name):
                    (print("\nINVALID: Please ensure item name has no spaces."))
                else:
                    break
            
            print("\nEnter quantity:")
            while True:
                quantity = str(input(">>> "))
                if quantity == "CANCEL":
                    return
                if re.search(r"^[0-9]+$", quantity):
                    break
                else:
                    print("\nERROR: Invalid quantity. Quantity must be a positive integer (1 and above).")
            
            print("\nEnter unit price: ")
            while True:
                unit_price = str(input(">>> "))
                if unit_price == "CANCEL":
                    return
                if re.search(r"^(?:\d+)?(?:\.\d+)?$", unit_price):
                    break
                else:
                    print("\nERROR: Invalid unit price. Please ensure that it is in correct format (e.g., 150, 250.46, 100.00)")

            new_node = ReceiptEntryNode(item_name, quantity, float(unit_price), ctr)

            if self.head is None:
                self.head = new_node
                self.tail = new_node
            else:
                self.tail.next_node = new_node
                new_node.previous_node = self.tail
                self.tail = new_node
            
            clear_console()

    def delete_entry(self):
        clear_console()

        if self.head:
            min_value = self.head.entry.entry_position
            max_value= self.tail.entry.entry_position

            while True:
                try:
                    choosen_option = str(input("(Type \"CANCEL\" to go back)\n\nType the position number of item you want to delete: "))
                    if choosen_option == "CANCEL":
                        return
                    else:
                        choosen_option = int(choosen_option)

                    if choosen_option >= min_value and choosen_option <= max_value:
                        if self.head and self.head.entry.entry_position == choosen_option:
                            self.head = self.head.next_node
                            if not self.head:
                                self.tail = None
                            self.update_entry_position(self.head)
                            return
                        else:
                            current = self.head
                            previous = None

                            while current:
                                if current.entry.entry_position == choosen_option:
                                    if previous:
                                        previous.next_node = current.next_node
                                        self.update_entry_position(current.next_node)
                                    if current == self.tail:
                                        self.tail = previous
                                    return
                                previous = current
                                current = current.next_node
                    else:
                        print("ERROR: Please enter a valid number to delete.")
                except ValueError:
                    print("ERROR: Please enter a valid number to delete.")
        else:
            print("\nERROR: Cannot delete as there is nothing to delete.")
            input("Press Enter to proceed...")

    def edit_entry_details(self):
        def change_item_name(node):
            clear_console()
            print(f"POS: {node.entry.entry_position}\nITEM NAME: {node.entry.item_name}\nQUANTITY: {node.entry.quantity}\nUNIT PRICE: {node.entry.unit_price}")
            new_name = str(input("\nEnter new item name:\n>>> "))
            print(f"\n\"{node.entry.item_name}\" will be changed into \"{new_name}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")

            while True:
                try:
                    option = int(input(">>> "))
                    if option == 1:
                        node.entry.item_name = new_name
                        return
                    elif option == 2:
                        return
                    else:
                        print("\nInvalid option. Please enter a number between 1 and 2.")
                except ValueError:
                    print("\nInvalid value. Please enter a correct number.")
        
        def change_quantity(node):
            clear_console()
            print(f"POS: {node.entry.entry_position}\nITEM NAME: {node.entry.item_name}\nQUANTITY: {node.entry.quantity}\nUNIT PRICE: {node.entry.unit_price}")
            
            print("\nEnter new quantity:")
            while True:
                new_quantity = str(input(">>> "))
                if re.search(r"^[0-9]+$", new_quantity):
                    break
                else:
                    print("\nERROR: Invalid quantity. Quantity must be a positive integer (1 and above).")
            
            print(f"\n{node.entry.item_name}\'s quantity will be changed from \"{node.entry.quantity}\" to \"{new_quantity}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")

            while True:
                try:
                    option = int(input(">>> "))
                    if option == 1:
                        node.entry.quantity = new_quantity
                        node.entry.total_price = node.compute_total_price(new_quantity, node.entry.unit_price)
                        return
                    elif option == 2:
                        return
                    else:
                        print("\nInvalid option. Please enter a number between 1 and 2.")
                except ValueError:
                    print("\nInvalid value. Please enter a correct number.")

        def change_unit_price(node):
            clear_console()
            print(f"POS: {node.entry.entry_position}\nITEM NAME: {node.entry.item_name}\nQUANTITY: {node.entry.quantity}\nUNIT PRICE: {node.entry.unit_price}")
            
            print("\nEnter new unit price:")
            while True:
                new_unit_price = str(input(">>> "))
                if re.search(r"^(?:\d+)?(?:\.\d+)?$", new_unit_price):
                    break
                else:
                    print("\nERROR: Invalid unit price. Please ensure that it is in correct format (e.g., 150, 250.46, 100.00)")
            
            print(f"\n{node.entry.item_name}\'s unit price will be changed from \"{node.entry.unit_price}\" to \"{float(new_unit_price)}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")

            while True:
                try:
                    option = int(input(">>> "))
                    if option == 1:
                        node.entry.unit_price = float(new_unit_price)
                        node.entry.total_price = node.compute_total_price(node.entry.quantity, float(new_unit_price))
                        return
                    elif option == 2:
                        return
                    else:
                        print("\nInvalid option. Please enter a number between 1 and 2.")
                except ValueError:
                    print("\nInvalid value. Please enter a correct number.")

        def choose_option(node):
            clear_console()
            print(f"POS: {node.entry.entry_position}\nITEM NAME: {node.entry.item_name}\nQUANTITY: {node.entry.quantity}\nUNIT PRICE: {node.entry.unit_price}")
            print("\nChoose option:\n1 = Edit item name\n2 = Edit quantity\n3 = Edit unit price\n4 = Go back\n\nChoose option:")
            while True:
                try:
                    choosen_option = int(input(">>> "))
                    if choose_option == 0:
                        return
                    if choosen_option == 1:
                        change_item_name(node)
                        return
                    if choosen_option == 2:
                        change_quantity(node)
                        return
                    if choosen_option == 3:
                        change_unit_price(node)
                        return
                    else:
                        print("\nERROR: Please enter a valid number between 1 and 3.")
                except ValueError:
                    print("\nERROR: Please enter a valid number between 1 and 3.")

        clear_console()

        if self.head:
            min_value = self.head.entry.entry_position
            max_value = self.tail.entry.entry_position

            print("(Type \"CANCEL\" to go back)\n\nType the position number of entry you want to change the details:")
            while True:
                try:
                    choosen_option = str(input(">>> "))
                    if choosen_option == "CANCEL":
                        return
                    else:
                        choosen_option = int(choosen_option)

                    if choosen_option >= min_value and choosen_option <= max_value:
                        current = self.head
                        while current:
                            if choosen_option == current.entry.entry_position:
                                choose_option(current)
                                return
                            current = current.next_node
                    else:
                        print("\nERROR: Please enter a valid number to change entry.")
                except ValueError:
                    print("\nERROR: Please enter a valid number to change entry.")
        else:
            print("\nERROR: Cannot edit as there is nothing to edit.")
            input("Press Enter to proceed...")

    def swap(self, node_1, node_2):
        node_1.item_name, node_2.item_name = node_2.item_name, node_1.item_name
        node_1.quantity, node_2.quantity = node_2.quantity, node_1.quantity
        node_1.unit_price, node_2.unit_price = node_2.unit_price, node_1.unit_price
        node_1.total_price, node_2.total_price = node_2.total_price, node_1.total_price

    def sort_list(self):
        clear_console()

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
        
        print("SUCCESS: Receipt entries sorted successfully.")
        input("Press Enter to proceed.")

    def change_receipt_header(self):
        def display_menu(self):
            clear_console()
            print(f"\nReceipt code: {self.receipt_number}")
            print(f"Date/time: {self.date}, {self.time}")
            print("\nChoose option:\n0 = Go back\n1 = Change receipt code\n2 = Change date\n3 = Change time")

        def change_receipt_code(self):
            clear_console()
            new_name = str(input("(Type \"CANCEL\" to go back)\n\nEnter new receipt code:\n>>> "))

            if new_name == "CANCEL":
                return

            print(f"\n\"{self.receipt_number}\" will be changed into \"{new_name}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")

            while True:
                try:
                    option = int(input(">>> "))
                    if option == 1:
                        self.receipt_number = new_name
                        break
                    elif option == 2:
                        return
                    else:
                        print("\nInvalid option. Please enter a number between 1 and 2.")
                except ValueError:
                    print("\nInvalid value. Please enter a correct number.")

        def change_date(self):
            clear_console()
            current_date = datetime.strptime(self.date, "%Y/%m/%d") if self.date else None

            print("(Type \"CANCEL\" to go back)\n\nEnter new date in YYYY/MM/DD format (e.g., 2024/05/20):")
            while True:
                new_date = str(input(">>> "))

                if new_date == "CANCEL":
                    return
                
                try:
                    filtered_date = datetime.strptime(new_date, "%Y/%m/%d")
                    break
                except ValueError:
                    print("\nERROR: Invalid date. Please ensure that date is in proper format YYYY/MM/DD format (e.g., 2024/05/20)")

            if current_date is not None:
                print(f"\n\"{current_date.strftime("%Y/%m/%d")}\" will be changed into \"{filtered_date.strftime("%Y/%m/%d")}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")
            else:
                print(f"\nNew date will be \"{filtered_date.strftime("%Y/%m/%d")}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")

            while True:
                try:
                    option = int(input(">>> "))
                    if option == 1:
                        self.date = str(filtered_date.strftime("%Y/%m/%d"))
                        break
                    elif option == 2:
                        return
                    else:
                        print("\nInvalid option. Please enter a number between 1 and 2.")
                except ValueError:
                    print("\nInvalid value. Please enter a correct number.")
            
        def change_time(self):
            clear_console()
            current_time = datetime.strptime(self.time, "%H:%M:%S") if self.time else None

            print("(Type \"CANCEL\" to go back)\n\nEnter new time in HH:MM:SS format (e.g., 20:01:59):")
            while True:
                new_time = str(input(">>> "))

                if new_time == "CANCEL":
                    return
                
                try:
                    filtered_time = datetime.strptime(new_time, "%H:%M:%S")
                    break
                except ValueError:
                    print("\nERROR: Invalid time. Please ensure that time is in proper HH:MM:SS format (e.g., 20:01:59)")

            if current_time is not None:
                print(f"\n\"{current_time.strftime("%H:%M:%S")}\" will be changed into \"{filtered_time.strftime("%H:%M:%S")}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")
            else:
                print(f"\nNew time will be \"{filtered_time.strftime("%H:%M:%S")}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")

            while True:
                try:
                    option = int(input(">>> "))
                    if option == 1:
                        self.time = str(filtered_time.strftime("%H:%M:%S"))
                        break
                    elif option == 2:
                        return
                    else:
                        print("\nInvalid option. Please enter a number between 1 and 2.")
                except ValueError:
                    print("\nInvalid value. Please enter a correct number.")
            
        display_menu(self)
        print("\nEnter option:")

        while True:
            try:
                option = int(input(">>> "))

                if option == 0:
                    return
                elif option == 1:
                    change_receipt_code(self)
                    break
                elif option == 2:
                    change_date(self)
                    break
                elif option == 3:
                    change_time(self)
                    break
                else:
                    print("\nInvalid option. Please enter a number between 1 and 4.")
            except ValueError:
                print("\nInvalid value. Please enter a correct number.")

    def update_entry_position(self, node):
        current = node

        while current:
            current.entry.entry_position -= 1
            current = current.next_node

if __name__ == "__main__":
    print("Please run the main.py to run the program.")
    input("Press Enter to exit...")
