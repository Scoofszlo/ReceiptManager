from receipt_checker import ReceiptEntryList

if __name__ == "__main__":
    print("Welcome to ReceiptChecker!")
    while True:
        try:
            choosen_num = int(input("Please choose a number on what you want to do:\n1 = Read from file\n2 = Enter entries manually.\n3 = Exit\n\nEnter num: "))

            if choosen_num == 1:
                r = ReceiptEntryList()
                file = str(input("\nEnter the filename including its extension (e.g., data.txt): "))
                try:
                    with open(file, "r") as file:
                        r.build_list_from_file(file)
                        # r.sort_list()
                        r.write_receipt_output_file()
                        break
                except FileNotFoundError:
                    print(f"ERROR: {file} is not found.")
                    exit(0)
                break
            elif choosen_num == 2:
                print("Code for this one will be written later.")
                break
            elif choosen_num == 3:
                print("The program will now exit.")
                break
        except ValueError:
            print("\nInvalid value. Please enter a correct number.")
