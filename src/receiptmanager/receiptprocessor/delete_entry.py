def delete_entry(receipt_obj, position):
    """
    If the entry to be deleted is located at the head or basically at the start of the
    receipt list, then it will be replaced by the node that is next to it. The code block
    (that has the if not receipt_obj.head) is important if the entry to be deleted is the
    only one existing at the receipt list.
    """
    if receipt_obj.head and receipt_obj.head.entry.entry_position == position:
        receipt_obj.head = receipt_obj.head.next_node
        if not receipt_obj.head:
            receipt_obj.tail = None
        __update_entry_position(receipt_obj.head)
        return
    
    else:
        current = receipt_obj.head
        previous = None

        while current:
            if current.entry.entry_position == position:
                if previous:
                    previous.next_node = current.next_node
                    __update_entry_position(current.next_node)
                if current == receipt_obj.tail:
                    receipt_obj.tail = previous
                return
            previous = current
            current = current.next_node

def __update_entry_position(node):
    current = node

    while current:
        current.entry.entry_position -= 1
        current = current.next_node
