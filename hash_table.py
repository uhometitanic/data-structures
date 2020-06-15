from collections.abc import MutableMapping
import typing

HashableItems = typing.Iterable[
    typing.Tuple[typing.Hashable, typing.Any]
]


def _probe_seq(key, list_len):
    """
    Generate the probing sequence of the key by the linear congruential generator:
        x = (5 * x + c) % list_len
    In order for the sequence to be a permutation of range(m),
    list_len must be a power of 2 and c must be odd.

    We choose to compute c by hashing str(key) prefixed with underscore and
        c = (2 * hashed_string - 1) % list_len
    so that c is always odd.
    This way two colliding keys would likely (but not always) have different probing sequences.
    """
    x = hash(key) % list_len
    yield x

    hashed_string = hash('_' + str(key))
    c = (2 * hashed_string - 1) % list_len

    for _ in range(list_len - 1):
        x = (5 * x + c) % list_len
        yield x


class HashTable(MutableMapping):
    """A hash table using linear congruential probing as the collision resolution.
    Under the hood we use a private list self._items to store the items.
    We rehash the items to a larger list (resp. smaller list) every time the original list
    becomes too crowded (resp. too sparse).
    For probing to work properly, len(self._items) must always be a power of 2.
    """
    # _init_size must be a power of 2 and not too large, 8 is reasonable
    _init_size = 8

    # a placeholder for any deleted item
    _placeholder = object()

    def __init__(self, items: typing.Optional[HashableItems] = None):
        """
        :argument:
        items (iterable of tuples): an iterable of (key, value) pairs
        """
        self._items = [None] * self._init_size
        self._len = 0

        if items is not None:
            for key, value in items:
                self[key] = value

    def __len__(self):
        """Return the number of items."""
        return self._len

    def __iter__(self):
        """Iterate over the keys."""
        for item in self._items:
            if item not in (None, self._placeholder):
                yield item[0]

    def __getitem__(self, key):
        """Get the value corresponding to the key.
        Raise KeyError if no such key found
        """
        probe = _probe_seq(key, len(self._items))
        idx = next(probe)

        # return the value if key found while probing self._items
        while self._items[idx] is not None:
            if (self._items[idx] is not self._placeholder
                    and self._items[idx][0] == key):
                return self._items[idx][1]
            idx = next(probe)

        raise KeyError

    @classmethod
    def _add(cls, key, value, items):
        """Helper function for __setitem__ to probe the items list.
        Return False if found the key and True otherwise.
        In either cases, set the value at the correct location.
        """
        loc = None
        probe = _probe_seq(key, len(items))
        idx = next(probe)

        while items[idx] is not None:
            # key found, set value at the same location
            if items[idx] is not cls._placeholder and items[idx][0] == key:
                items[idx] = (key, value)
                return False

            # remember the location of the first placeholder found during probing
            if loc is None and items[idx] is cls._placeholder:
                loc = idx

            idx = next(probe)

        # key not found, set the item at the location of the first placeholder
        # or at the location of None at the end of the probing sequence
        if loc is None:
            loc = idx
        items[loc] = (key, value)

        return True

    @classmethod
    def _rehash(cls, old_list, new_list):
        """Rehash the items from old_list to new_list"""
        for item in old_list:
            if item not in (None, cls._placeholder):
                cls._add(*item, new_list)

        return new_list

    def __setitem__(self, key, value):
        """Set self[key] to be value.
        Overwrite the old value if key found.
        """
        # key not found, add one item
        if self._add(key, value, self._items):
            self._len += 1
            if self._len / len(self._items) > 0.75:
                # too crowded, rehash to a larger list
                # resizing factor is 2 so that the length remains a power of 2
                new_list = [None] * (len(self._items) * 2)
                self._items = self._rehash(self._items, new_list)

    @classmethod
    def _remove(cls, key, items):
        """Helper function for __delitem__ to probe the items list.
        Return False if key not found.
        Otherwise, delete the item and return True.
        (Note that this is opposite to _add because
        for _add, returning True means an item has been added, while
        for _remove, returning True means an item has been removed.)
        """
        probe = _probe_seq(key, len(items))
        idx = next(probe)

        while items[idx] is not None:
            next_idx = next(probe)

            # key found, replace the item with the placeholder
            if items[idx] is not cls._placeholder and items[idx][0] == key:
                items[idx] = cls._placeholder
                return True

            idx = next_idx

        return False

    def __delitem__(self, key):
        """Delete self[key].
        Raise KeyError if no such key found.
        """
        # key found, remove one item
        if self._remove(key, self._items):
            self._len -= 1
            numerator = max(self._len, self._init_size)

            if numerator / len(self._items) < 0.25:
                # too sparse, rehash to a smaller list
                # resizing factor is 1/2 so that the length remains a power of 2
                new_list = [None] * (len(self._items) // 2)
                self._items = self._rehash(self._items, new_list)

        else:
            raise KeyError
