import ctypes
import math

class ListNode:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def search(self, key):
        x = self.head
        while x is not None and x.key != key:
            x = x.next
        return x

    def insert(self, key, value):
        x = ListNode(key, value)
        x.next = self.head
        if self.head is not None:
            self.head.prev = x
        self.head = x
        x.prev = None

    def delete(self, key):
        x = self.search(key)
        if x is None:
            return False
        if x.prev is not None:
            x.prev.next = x.next
        else:
            self.head = x.next
        if x.next is not None:
            x.next.prev = x.prev
        return True

    def items(self):
        x = self.head
        while x is not None:
            yield x.key, x.value
            x = x.next


class HashTable:
    def __init__(self, initial_capacity=8, hash_func=None):
        self.size = 0
        self.capacity = initial_capacity
        self.hash_func = hash_func or self.hash_division
        self.table = self.make_array(self.capacity)

    def make_array(self, capacity):
        array = (ctypes.py_object * capacity)()
        for i in range(capacity):
            array[i] = DoublyLinkedList()
        return array

    # Division method
    def hash_division(self, key):
        return key % self.capacity

    # Multiplication method
    def hash_multiplication(self, key):
        A = (math.sqrt(5) - 1) / 2
        return int(self.capacity * ((key * A) % 1))

    def resize(self, new_capacity):
        old_items = list(self.items())
        self.capacity = new_capacity
        self.table = self.make_array(self.capacity)
        self.size = 0
        for key, value in old_items:
            self.insert(key, value)

    def insert(self, key, value):
        if self.size >= self.capacity:
            self.resize(self.capacity * 2)
        index = self.hash_func(key)
        if self.table[index].search(key) is None:
            self.size += 1
        self.table[index].insert(key, value)

    def delete(self, key):
        index = self.hash_func(key)
        deleted = self.table[index].delete(key)
        if deleted:
            self.size -= 1
            if self.capacity > 8 and self.size <= self.capacity // 4:
                self.resize(self.capacity // 2)
        return deleted

    def search(self, key):
        index = self.hash_func(key)
        node = self.table[index].search(key)
        return node.value if node else None

    def items(self):
        for chain in self.table:
            yield from chain.items()


if __name__ == "__main__":
    #should print and prints:
        # 900
        # None
        # 4200

    # Using division hash function by default
    ht = HashTable(hash_func=None)

    # all of these 3 inserts go on slot 1
    ht.insert(1, 100)
    ht.insert(9, 900)
    ht.insert(17, 1700)

    #prints value of 900 after finding 9
    print(ht.search(9))
    #delete operation on key 9
    ht.delete(9)
    #prints None since the key 9 is not available anymore
    print(ht.search(9))

    # Switching to the multiplication hash function
    ht.hash_func = ht.hash_multiplication
    #inserting at slot 7
    ht.insert(42, 4200)
    # finds 42 and returns its value 4200
    print(ht.search(42))