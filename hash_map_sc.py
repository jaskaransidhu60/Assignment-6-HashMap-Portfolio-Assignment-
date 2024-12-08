# Name: Jaskaran Singh Sidhu
# OSU Email: sidhuja@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap Implementation
# Description: This file implements a HashMap using Separate Chaining for collision resolution.
# It includes methods for put, get, remove, resizing, and finding mode in a dynamic array.

from a6_include import DynamicArray, LinkedList, hash_function_1, hash_function_2

class HashMap:
    def __init__(self, capacity: int = 11, function=hash_function_1):
        """
        Initialize HashMap with given capacity and hash function.
        """
        self._buckets = DynamicArray()
        self._capacity = self._next_prime(capacity)
        self._hash_function = function
        self._size = 0
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

    def put(self, key: str, value: object) -> None:
        """
        Add a key-value pair to the hash map. Update value if key exists.
        Resize the table if the load factor >= 1.0.
        """
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)
        
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        
        node = bucket.contains(key)
        if node:
            node.value = value
        else:
            bucket.insert(key, value)
            self._size += 1

    def get(self, key: str):
        """
        Return value associated with the key, or None if not found.
        """
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        node = bucket.contains(key)
        return node.value if node else None

    def remove(self, key: str) -> None:
        """
        Remove the key-value pair from the hash map.
        """
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        if bucket.remove(key):
            self._size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Check if the key exists in the hash map.
        """
        return self.get(key) is not None

    def table_load(self) -> float:
        """
        Return the current load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets.
        """
        return sum(1 for i in range(self._capacity) if self._buckets[i].length() == 0)

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize the hash table to the next prime greater than new_capacity.
        """
        if new_capacity < self._size:
            return
        new_capacity = self._next_prime(new_capacity)
        old_buckets = self._buckets

        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        for i in range(old_buckets.length()):
            for node in old_buckets[i]:
                self.put(node.key, node.value)

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a DynamicArray containing all key-value pairs.
        """
        result = DynamicArray()
        for i in range(self._capacity):
            for node in self._buckets[i]:
                result.append((node.key, node.value))
        return result

    def clear(self) -> None:
        """
        Clear all key-value pairs from the hash map.
        """
        for i in range(self._capacity):
            self._buckets[i] = LinkedList()
        self._size = 0

    @staticmethod
    def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
        """
        Return the mode(s) of the input DynamicArray and their frequency.
        """
        map = HashMap()
        max_frequency = 0
        result = DynamicArray()

        for value in da:
            count = map.get(value)
            count = count + 1 if count else 1
            map.put(value, count)
            if count > max_frequency:
                max_frequency = count

        for key, value in map.get_keys_and_values():
            if value == max_frequency:
                result.append(key)
        return result, max_frequency

    def _next_prime(self, capacity: int) -> int:
        """
        Return the next prime number >= capacity.
        """
        if capacity % 2 == 0:
            capacity += 1
        while not self._is_prime(capacity):
            capacity += 2
        return capacity

    @staticmethod
    def _is_prime(n: int) -> bool:
        """
        Check if a number is prime.
        """
        if n < 2 or n % 2 == 0:
            return n == 2
        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                return False
        return True


# ------------------- BASIC TESTING ---------------------------------------- #
if __name__ == "__main__":
    m = HashMap(11, hash_function_1)
    m.put('key1', 10)
    print(m.get('key1'))  # Output: 10
    m.put('key1', 20)
    print(m.get('key1'))  # Output: 20
    print(m.contains_key('key2'))  # Output: False
    print(m.empty_buckets())  # Output: 10
    m.resize_table(20)
    print(m.get_keys_and_values())  # Output: [('key1', 20)]
    da = DynamicArray(["a", "b", "a", "c", "b", "b"])
    print(HashMap.find_mode(da))  # Output: (['b'], 3)
