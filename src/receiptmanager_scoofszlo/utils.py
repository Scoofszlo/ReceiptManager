import os
from decimal import Decimal, ROUND_HALF_UP

def round_num(value):
    num = Decimal(str(value))
    rounded_num = num.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return float(rounded_num)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[H", end="")
