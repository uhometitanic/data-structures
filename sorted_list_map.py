# sorted_list_map.py

from collections.abc import MutableMapping
import typing

HashableItems = typing.Iterable[
    typing.Tuple[typing.Hashable, typing.Any]
]


def _binary_search(items, key):
    """A helper function that finds the relative position of the given key in the list of
    (key, value) pairs, in which the keys are distinct and already sorted.
    Return a pair of indices in which the first one is the immediate predecessor index before
    the given key and the second one is the immediate successor index after the given key.
    If key is found, then the two indices differ by 1, otherwise they differ by 2.
    """
    left, right = 0, len(items) - 1

    while left <= right:
        mid_idx = (left + right) // 2
        mid_key = items[mid_idx][0]

        if key == mid_key:
            # if key is found at mid_idx, then predecessor is immediately before mid_idx
            # and successor is immediately after mid_idx
            return mid_idx - 1, mid_idx + 1
        elif key < mid_key:
            right = mid_idx - 1
        else:
            left = mid_idx + 1

    # key not found, at this point right is smaller than left by 1
    # right is the predecessor and left is the successor
    return right, left


class SortedListMap(MutableMapping):
    """Implement a sorted list as a sorted map.
    The keys must have a total ordering (i.e. any two keys can be compared).
    """

    def __init__(self, items: typing.Optional[HashableItems] = None):
        """
        :argument:
        items (iterable of tuples): an iterable of (key, value) pairs
        """
        self._items = []
        if items is not None:
            for key, value in items:
                self[key] = value

    def __len__(self):
        """Return the number of items."""
        return len(self._items)

    def __iter__(self):
        """Iterate over the keys in ascending order."""
        for key, _ in self._items:
            yield key

    """Ordering methods"""

    def minimum(self):
        """Return the (key, value) pair with the minimum key.
        Raise a KeyError if the list is empty.
        """
        if len(self) == 0:
            raise KeyError('empty list')
        else:
            return self._items[0]

    def maximum(self):
        """Return the (key, value) pair with the maximum key.
        Raise a KeyError if the list is empty.
        """
        if len(self) == 0:
            raise KeyError('empty list')
        else:
            return self._items[-1]

    def predecessor(self, key):
        """Return the (key, value) pair with the largest key that is strictly
        less than the given key, regardless of whether the given key exists in the list.
        Raise a KeyError if the list is empty or no key is strictly less than the given key.
        """
        if len(self) == 0:
            raise KeyError('empty list')

        pred_idx, _ = _binary_search(self._items, key)
        if pred_idx == -1:
            raise KeyError(f'No key less than {key}')
        else:
            return self._items[pred_idx]

    def successor(self, key):
        """Return the (key, value) pair with the smallest key that is strictly
        greater than the given key, regardless of whether the given key exists in the list.
        Raise a KeyError if the list is empty or no key is strictly greater than the given key.
        """
        if len(self) == 0:
            raise KeyError('empty list')

        _, succ_idx = _binary_search(self._items, key)
        if succ_idx == len(self):
            raise KeyError(f'No key greater than {key}')
        else:
            return self._items[succ_idx]

    """Accessor methods"""

    def __getitem__(self, key):
        """Get the value corresponding to the key.
        Raise a KeyError if no such key found.
        """
        pred_idx, succ_idx = _binary_search(self._items, key)
        if succ_idx - pred_idx == 1:
            raise KeyError(f'key {key} not found')
        else:
            return self._items[pred_idx + 1][1]

    def __setitem__(self, key, value):
        """Set self[key] to be value.
        Overwrite the old value if key found.
        """
        pred_idx, succ_idx = _binary_search(self._items, key)
        if succ_idx - pred_idx == 1:
            self._items.insert(succ_idx, (key, value))
        else:
            self._items[pred_idx + 1] = (key, value)

    def __delitem__(self, key):
        """Delete self[key].
        Raise a KeyError if no such key found.
        """
        pred_idx, succ_idx = _binary_search(self._items, key)
        if succ_idx - pred_idx == 1:
            raise KeyError(f'key {key} not found')
        else:
            self._items.pop(pred_idx + 1)
