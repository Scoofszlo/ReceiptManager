from src.receiptmanager.constants import CURRENCY
from src.receiptmanager.utils import clear_console, round_num

def is_receipt_list_empty(receipt_obj):
    if receipt_obj.head:
        return None
    return True

def get_lowest_idx_pos(receipt_obj):
    return receipt_obj.head.entry.entry_position

def get_highest_idx_pos(receipt_obj):
    return receipt_obj.tail.entry.entry_position

def get_currency(config):
    return config["currency"]

def get_currency_symbol(config):
    currency_abbreviation = get_currency(config)
    return CURRENCY[currency_abbreviation]["symbol"]

def display_config(config_file):
    user_preferred_currency = config_file["currency"]
    user_preferred_currency_in_symbol = get_currency_symbol(config_file)

    if user_preferred_currency_in_symbol is not None:
        print(f"\"currency\": {user_preferred_currency} ({user_preferred_currency_in_symbol}) - {CURRENCY[user_preferred_currency]["currency_word"]}")
    else:
        print("\"currency\": NO_CURRENCY_USED")

def display_entries(receipt_obj):
    clear_console()

    spacing_values = get_spacing_values_length(receipt_obj) # Sets the spacing values between columns
    total_price = 0.0 # Used to put the total price of all entries
    total_of_items = 0 # Used to put the total number of items
    current = receipt_obj.head # Used to navigate through the list of entries by starting at the first index


    # This is the area that prints the preview of entries as well as other important receipt details
    print("-" * spacing_values[5]) # Prints the dash lines at the top for styling purposes
    if not current:
        print("LIST IS CURRENTLY EMPTY.\nReceipt entries will be previewed here.")
    else:
        date = receipt_obj.date if receipt_obj.date else "<N0_RECEIPT_DATE>"
        time = receipt_obj.time if receipt_obj.time else "<NO_RECEIPT_TIME>"
        formatted_receipt_number = receipt_obj.receipt_code if receipt_obj.receipt_code else "<NO_RECEIPT_CODE>"

        print("{:^{}}".format(
            "RECEIPT CODE: " + formatted_receipt_number, spacing_values[5]
        ))

        print("{:^{}}".format(
            "DATE & TIME: " + date + ", " + time, spacing_values[5]
        ))


        column_header = ["POS", "ITEM NAME", "QUANTITY", "UNIT PRICE", "TOTAL PRICE"]
        print("\n{:<{}} {:>{}} {:>{}} {:>{}} {:>{}}".format(
            column_header[0], spacing_values[0] + 2,
            column_header[1], spacing_values[1] + 2,
            column_header[2], spacing_values[2] + 2,
            column_header[3], spacing_values[3] + 2,
            column_header[4], spacing_values[4] + 2
        ))

        # Gets the currency set from the config
        user_preferred_currency = receipt_obj.config["currency"]
        currency = CURRENCY[user_preferred_currency]["symbol"]

        while current is not None:
            formatted_quantity = f"{int(current.entry.quantity):,}"
            formatted_unit_price = f"{currency}{float(current.entry.unit_price):,.2f}" if currency else f"{float(current.entry.unit_price):,.2f}"
            formatted_total_price = f"{currency}{float(current.entry.total_price):,.2f}" if currency else f"{float(current.entry.total_price):,.2f}"
            print("{:<{}} {:>{}} {:>{}} {:>{}} {:>{}}".format(
                current.entry.entry_position, spacing_values[0] + 2,
                current.entry.item_name, spacing_values[1] + 2,
                formatted_quantity, spacing_values[2] + 2,
                formatted_unit_price, spacing_values[3] + 2,
                formatted_total_price, spacing_values[4] + 2
            ))

            total_price += current.entry.total_price

            total_price = round_num(total_price)
            total_of_items += 1

            current = current.next_node

        if total_of_items > 1 or total_of_items == 0:
            item_string = "items"
        else:
            item_string = "item"

        if user_preferred_currency:
            print(f"\nTOTAL SUM: {currency}{total_price:,.2f} ({total_of_items} {item_string})")
        else:
            print(f"\nTOTAL SUM: {total_price:,.2f} ({total_of_items} {item_string})")

    print("-" * spacing_values[5])

def get_spacing_values_length(receipt_obj):
    position_max_length = 3
    item_name_max_length = 9
    quantity_max_length = 8
    unit_price_max_length = 10
    total_price_max_length = 11

    current = receipt_obj.head

    while current is not None:
        item_name_max_length = max(item_name_max_length, len(current.entry.item_name))
        quantity_max_length = max(quantity_max_length, len(current.entry.quantity))
        unit_price_max_length = max(unit_price_max_length, len(str(current.entry.unit_price)))
        total_price_max_length = max(total_price_max_length, len(str(current.entry.total_price)))

        current = current.next_node

    spaces_total_length = 14 + position_max_length + item_name_max_length + quantity_max_length + unit_price_max_length + total_price_max_length
    return [position_max_length, item_name_max_length, quantity_max_length, unit_price_max_length, total_price_max_length, spaces_total_length]
