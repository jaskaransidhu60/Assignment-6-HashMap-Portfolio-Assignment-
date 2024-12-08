# Name: Jaskaran Singh Sidhu
# OSU Email: sidhuja@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap Implementation
# Due Date: Dec 5
# Description: This file implements a HashMap using Separate Chaining for collision resolution.
# It includes methods to insert, delete, search, and resize the table, among other utility methods.

from a6_include import (DynamicArray, LinkedList, hash_function_1, hash_function_2)

class HashMap:
    def __init__(self, capacity: int = 11, function: callable = hash_function_1) -> None:
        """
        Initialize a HashMap using Separate Chaining.
        """
        self._buckets = DynamicArray()
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        self._hash_function = function
        self._size = 0

    def _next_prime(self, capacity: int) -> int:
        if capacity % 2 == 0:
            capacity += 1
        while not self._is_prime(capacity):
            capacity += 2
        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        if capacity < 2 or capacity % 2 == 0:
            return False
        for i in range(3, int(capacity ** 0.5) + 1, 2):
            if capacity % i == 0:
                return False
        return True

    def put(self, key: str, value: object) -> None:
        """
        Insert or update a key-value pair in the HashMap.
        """
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[index]

        node = linked_list.contains(key)
        if node:
            node.value = value
        else:
            linked_list.insert(key, value)
            self._size += 1

    def get(self, key: str):
        """
        Return the value associated with the given key, or None if not found.
        """
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[index]
        node = linked_list.contains(key)
        return node.value if node else None

    def remove(self, key: str) -> None:
        """
        Remove a key-value pair from the HashMap.
        """
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[index]
        if linked_list.remove(key):
            self._size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Check if a key exists in the HashMap.
        """
        return self.get(key) is not None

    def clear(self) -> None:
        """
        Clear all key-value pairs from the HashMap.
        """
        for i in range(self._capacity):
            self._buckets[i] = LinkedList()
        self._size = 0

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets.
        """
        return sum(1 for i in range(self._capacity) if self._buckets[i].length() == 0)

    def table_load(self) -> float:
        """
        Return the current load factor of the HashMap.
        """
        return self._size / self._capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize the HashMap to a new capacity and rehash all key-value pairs.
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
        Return a DynamicArray containing all key-value pairs in the HashMap.
        """
        result = DynamicArray()
        for i in range(self._capacity):
            for node in self._buckets[i]:
                result.append((node.key, node.value))
        return result

    @staticmethod
    def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
        """
        Find the mode(s) in a DynamicArray and their frequency.
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
