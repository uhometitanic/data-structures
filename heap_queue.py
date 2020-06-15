class HeapQueue:
    """Implement a priority queue in the form of a min-heap.
    Each entry is an (item, key) pair. Item with a lower key has a higher priority.
    Item must be hashable and unique. No duplicate items.
    Pushing an existing item would update its key instead.
    """

    def __init__(self, entries=None):
        """
        :argument:
        entries (iterable of tuples): an iterable of (item, key) pairs
        """
        if entries is None:
            self._entries = []
            self._indices = {}
        else:
            self._entries = list(entries)
            self._indices = {item: idx for idx, (item, _) in enumerate(self._entries)}
            self._heapify()

    def _heapify(self):
        """Enforce the heap properties upon initializing the heap."""
        start = len(self) // 2 - 1
        for idx in range(start, -1, -1):
            self._down(idx)

    def __contains__(self, item):
        """Return True if the item is in the heap."""
        return item in self._indices

    def __len__(self):
        """Number of entries remaining in the heap."""
        return len(self._entries)

    def __iter__(self):
        """Iterate over all items."""
        for item, _ in self._entries:
            yield item

    """Helper methods"""

    def _swap(self, idx1, idx2):
        """Swap two entries."""
        item1, _ = self._entries[idx1]
        item2, _ = self._entries[idx2]
        self._indices[item1] = idx2
        self._indices[item2] = idx1
        self._entries[idx1], self._entries[idx2] = self._entries[idx2], self._entries[idx1]

    def _up(self, idx):
        """Bring a violating entry up to its correct position recursively."""
        if idx == 0:
            return

        parent = (idx - 1) // 2
        # compare key with the parent
        if self._entries[idx][1] < self._entries[parent][1]:
            self._swap(idx, parent)
            self._up(parent)

    def _smaller_child(self, idx):
        """Find the child with smaller key. If no child, return None."""
        left = 2 * idx + 1
        # case 1: no child
        if left >= len(self):
            return None

        right = left + 1
        # case 2: only left child
        if right == len(self):
            return left

        # case 3: two children
        if self._entries[left][1] < self._entries[right][1]:
            return left
        else:
            return right

    def _down(self, idx):
        """Bring a violating entry down to its correct position recursively."""
        child = self._smaller_child(idx)
        if child is None:
            return

        # compare key with the child with smaller key
        if self._entries[idx][1] > self._entries[child][1]:
            self._swap(idx, child)
            self._down(child)

    """Priority queue operations"""

    def __getitem__(self, item):
        """Return the key of an item.
        If the item does not exist, raise a KeyError."""
        if item not in self._indices:
            raise KeyError(f"{item} not found")

        idx = self._indices[item]
        _, key = self._entries[idx]
        return key

    def peek(self):
        """Return the item with the minimum key."""
        item, _ = self._entries[0]
        return item

    def push(self, item, key):
        """Push an item into the heap with a given key.
        If the item already exists, update its key instead.
        """
        if item not in self._indices:
            # insert the new item to the end and bring it up to the correct position
            idx = len(self)
            self._entries.append((item, key))
            self._indices[item] = idx
            self._up(idx)
        else:
            # the item already exists, find its index and update its key
            idx = self._indices[item]
            item, old_key = self._entries[idx]
            self._entries[idx] = (item, key)

            # bring the entry to the correct position
            if key < old_key:
                self._up(idx)
            if key > old_key:
                self._down(idx)

    def pop(self):
        """Remove the item with the minimum key.
        The resulting (item, key) pair is also returned."""
        # after swapping the first and the last entry,
        # the required entry goes from the beginning to the end
        self._swap(0, len(self) - 1)
        item, key = self._entries.pop()

        del self._indices[item]
        self._down(0)
        return item, key
