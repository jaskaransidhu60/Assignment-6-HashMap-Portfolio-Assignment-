from a6_include import DynamicArray, HashEntry, hash_function_1


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        self._buckets = DynamicArray()
        self._capacity = self._next_prime(capacity)
        self._hash_function = function
        self._size = 0

        for _ in range(self._capacity):
            self._buckets.append(None)

    def get_capacity(self) -> int:
        """
        Return the current capacity of the hash map.
        """
        return self._capacity

    def get_size(self) -> int:
        """
        Return the current size (number of elements) of the hash map.
        """
        return self._size

    def _find_slot(self, key: str) -> int:
        index = self._hash_function(key) % self._capacity
        for i in range(self._capacity):
            probe = (index + i**2) % self._capacity
            entry = self._buckets.get_at_index(probe)
            if entry is None or entry.key == key or entry.is_tombstone:
                return probe
        return -1

    def put(self, key: str, value: object) -> None:
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
        slot = self._find_slot(key)
        entry = self._buckets.get_at_index(slot)
        return entry.value if entry and not entry.is_tombstone else None

    def contains_key(self, key: str) -> bool:
        slot = self._find_slot(key)
        entry = self._buckets.get_at_index(slot)
        return entry is not None and not entry.is_tombstone

    def remove(self, key: str) -> None:
        slot = self._find_slot(key)
        entry = self._buckets.get_at_index(slot)
        if entry and not entry.is_tombstone:
            entry.is_tombstone = True
            self._size -= 1

    def table_load(self) -> float:
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        return sum(1 for i in range(self._capacity)
                   if self._buckets.get_at_index(i) is None or self._buckets.get_at_index(i).is_tombstone)

    def resize_table(self, new_capacity: int) -> None:
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
        result = DynamicArray()
        for i in range(self._capacity):
            entry = self._buckets.get_at_index(i)
            if entry and not entry.is_tombstone:
                result.append((entry.key, entry.value))
        return result

    def clear(self) -> None:
        for i in range(self._capacity):
            self._buckets.set_at_index(i, None)
        self._size = 0

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        while self._index < self._capacity:
            entry = self._buckets.get_at_index(self._index)
            self._index += 1
            if entry and not entry.is_tombstone:
                return entry
        raise StopIteration

    def _next_prime(self, n: int) -> int:
        if n % 2 == 0:
            n += 1
        while not self._is_prime(n):
            n += 2
        return n

    @staticmethod
    def _is_prime(n: int) -> bool:
        if n < 2 or n % 2 == 0:
            return n == 2
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True
