# Name: Jaskaran Singh Sidhu
# OSU Email: sidhuja@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - Open Addressing HashMap Implementation
# Description: Implements a HashMap using Open Addressing with Quadratic Probing.
# It includes put, resize, load factor management, and iterator functionality.

from hash_map_oa import HashMap
from a6_include import hash_function_1


def find_mode(da: object) -> tuple:
    """
    Find the mode(s) and frequency using HashMap (Open Addressing).
    """
    map = HashMap(11, hash_function_1)
    max_frequency = 0
    modes = []

    for i in range(da.length()):
        value = da.get_at_index(i)
        if map.contains_key(value):
            count = map.get(value) + 1
            map.put(value, count)
        else:
            count = 1
            map.put(value, count)

        if count > max_frequency:
            max_frequency = count
            modes = [value]
        elif count == max_frequency:
            if value not in modes:
                modes.append(value)

    return modes, max_frequency
