"""Functions that are used throughout the program."""
import os
from decimal import Decimal, ROUND_HALF_UP

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[H", end="")

def round_num(value):
    num = Decimal(str(value))
    rounded_num = num.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return float(rounded_num)

def is_path_exists(path):
    if os.path.exists(path):
        return True
    else:
        return False

def create_folder_path(path):
    os.makedirs(path)
