# Name: Jaskaran Singh Sidhu
# OSU Email: sidhuja@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap Implementation
# Due Date: Dec 5
# Description: This file implements a HashMap using Open Addressing with Quadratic Probing.
# It includes methods to insert, delete, search, and resize the table.

from a6_include import (DynamicArray, HashEntry, hash_function_1, hash_function_2)

class HashMap:
    def __init__(self, capacity: int, function) -> None:
        self._buckets = DynamicArray()
        self._capacity = self._next_prime(capacity)
        self._size = 0
        self._hash_function = function
        for _ in range(self._capacity):
            self._buckets.append(None)

    def put(self, key: str, value: object) -> None:
        index = self._hash_function(key) % self._capacity
        i = 0
        while True:
            probe = (index + i ** 2) % self._capacity
            entry = self._buckets.get_at_index(probe)

            if entry is None or entry.is_tombstone:
                self._buckets.set_at_index(probe, HashEntry(key, value))
                self._size += 1
                return
            elif entry.key == key:
                entry.value = value
                return
            i += 1

    def get(self, key: str):
        index = self._hash_function(key) % self._capacity
        i = 0
        while True:
            probe = (index + i ** 2) % self._capacity
            entry = self._buckets.get_at_index(probe)
            if entry is None:
                return None
            if entry.key == key and not entry.is_tombstone:
                return entry.value
            i += 1
