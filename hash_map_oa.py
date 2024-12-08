# Name: Jaskaran Singh Sidhu
# OSU Email: sidhuja@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - Open Addressing HashMap Implementation
# Description: Implements a HashMap using Open Addressing with Quadratic Probing.
# It includes put, resize, load factor management, and iterator functionality.

from a6_include import DynamicArray, HashEntry, hash_function_1, hash_function_2


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize a HashMap with quadratic probing for collision resolution.
        """
        self._buckets = DynamicArray()
        self._capacity = self._next_prime(capacity)
        self._hash_function = function
        self._size = 0

        for _ in range(self._capacity):
            self._buckets.append(None)

    def _find_slot(self, key: str) -> int:
        """
        Return the index of a slot where the key belongs or can be inserted.
        """
        index = self._hash_function(key) % self._capacity
        for i in range(self._capacity):
            probe = (index + i**2) % self._capacity
            entry = self._buckets.get_at_index(probe)
            if entry is None or entry.key == key or entry.is_tombstone:
                return probe
        return -1

    def put(self, key: str, value: object) -> None:
        """
        Insert or update a key-value pair in the hash map.
        Resizes table if load factor exceeds 0.5.
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        slot = self._find_slot(key)
        entry = self._buckets.get_at_index(slot)
        if entry is None or entry.is_tombstone:
            self._buckets.set_at_index(slot, HashEntry(key, value))
            self._size += 1
        else:
            entry.value = value

    def get(self, key: str) -> object:
        """
        Return the value associated with the given key, or None if not found.
        """
        slot = self._find_slot(key)
        entry = self._buckets.get_at_index(slot)
        return entry.value if entry and not entry.is_tombstone else None

    def contains_key(self, key: str) -> bool:
        """
        Return True if key is in the hash map, False otherwise.
        """
        slot = self._find_slot(key)
        entry = self._buckets.get_at_index(slot)
        return entry is not None and not entry.is_tombstone

    def remove(self, key: str) -> None:
        """
        Remove the key-value pair from the hash map.
        """
        slot = self._find_slot(key)
        entry = self._buckets.get_at_index(slot)
        if entry and not entry.is_tombstone:
            entry.is_tombstone = True
            self._size -= 1

    def table_load(self) -> float:
        """
        Return the load factor of the hash map.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets.
        """
        return sum(1 for i in range(self._capacity)
                   if self._buckets.get_at_index(i) is None or self._buckets.get_at_index(i).is_tombstone)

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize the table to a new capacity and rehash all existing keys.
        """
        if new_capacity < self._size:
            return

        new_capacity = self._next_prime(new_capacity)
        old_buckets = self._buckets
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0

        for _ in range(new_capacity):
            self._buckets.append(None)

        for i in range(old_buckets.length()):
            entry = old_buckets.get_at_index(i)
            if entry and not entry.is_tombstone:
                self.put(entry.key, entry.value)

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a dynamic array of key-value pairs in the hash map.
        """
        result = DynamicArray()
        for i in range(self._capacity):
            entry = self._buckets.get_at_index(i)
            if entry and not entry.is_tombstone:
                result.append((entry.key, entry.value))
        return result

    def clear(self) -> None:
        """
        Clear all key-value pairs from the hash map.
        """
        for i in range(self._capacity):
            self._buckets.set_at_index(i, None)
        self._size = 0

    def __iter__(self):
        """
        Iterator for HashMap.
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Move to the next active element in the hash map.
        """
        while self._index < self._capacity:
            entry = self._buckets.get_at_index(self._index)
            self._index += 1
            if entry and not entry.is_tombstone:
                return entry
        raise StopIteration

    def _next_prime(self, n: int) -> int:
        """
        Return the next prime number greater than or equal to n.
        """
        if n % 2 == 0:
            n += 1
        while not self._is_prime(n):
            n += 2
        return n

    @staticmethod
    def _is_prime(n: int) -> bool:
        """
        Check if a number is prime.
        """
        if n < 2 or n % 2 == 0:
            return n == 2
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True


# ------------------- BASIC TESTING ---------------------------------------- #
if __name__ == "__main__":
    m = HashMap(10, hash_function_1)
    m.put("key1", 10)
    print(m.get("key1"))  # Output: 10
    m.put("key1", 20)
    print(m.get("key1"))  # Output: 20
    print(m.contains_key("key1"))  # Output: True
    print(m.empty_buckets())  # Output: 9
    m.remove("key1")
    print(m.contains_key("key1"))  # Output: False
