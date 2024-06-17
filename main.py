from receipt_checker import ReceiptEntryList

if __name__ == "__main__":
    r = ReceiptEntryList()
    r.build_list_from_file()
    r.sort_list()
    r.write_receipt_output_file()
