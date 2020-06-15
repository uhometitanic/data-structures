# binary_search_tree.py

from collections.abc import MutableMapping
import typing

HashableItems = typing.Iterable[
    typing.Tuple[typing.Hashable, typing.Any]
]


class BinarySearchTree(MutableMapping):
    """Implement a binary search tree as a sorted map.
    The keys must have a total ordering (i.e. any two keys can be compared).
    Under the hood the items are stored in the private class _BinaryNode.
    Most methods in this class just delegate the real works to _BinaryNode.
    """

    def __init__(self, items: typing.Optional[HashableItems] = None):
        """
        :argument:
        items (iterable of tuples): an iterable of (key, value) pairs
        """
        self._root = None
        self._len = 0

        if items is not None:
            for key, value in items:
                self[key] = value

    def __len__(self):
        """Return the number of items."""
        if self._root is None:
            return 0
        else:
            return self._root.length

    def __iter__(self):
        """Iterate over the keys in ascending order."""
        if self._root is None:
            yield from []
        else:
            for node in self._root:
                yield node.key

    """Ordering methods"""

    def minimum(self):
        """Return the (key, value) pair with the minimum key.
        Raise a KeyError if the tree is empty.
        """
        if self._root is None:
            raise KeyError('empty tree')
        else:
            min_node = self._root.minimum()
            return min_node.key, min_node.value

    def maximum(self):
        """Return the (key, value) pair with the maximum key
        Raise a KeyError if the tree is empty.
        """
        if self._root is None:
            raise KeyError('empty tree')
        else:
            max_node = self._root.maximum()
            return max_node.key, max_node.value

    def predecessor(self, key):
        """Return the (key, value) pair with the largest key that is strictly
        less than the given key, regardless of whether the given key exists in the tree.
        Raise a KeyError if the tree is empty or no key is strictly less than the given key.
        """
        if self._root is None:
            raise KeyError('empty tree')
        else:
            pred_node = self._root.predecessor(key)
            return pred_node.key, pred_node.value

    def successor(self, key):
        """Return the (key, value) pair with the smallest key that is strictly
        greater than the given key, regardless of whether the given key exists in the tree.
        Raise a KeyError if the tree is empty or no key is strictly greater than the given key.
        """
        if self._root is None:
            raise KeyError('empty tree')
        else:
            succ_node = self._root.successor(key)
            return succ_node.key, succ_node.value

    """Accessor methods"""

    def __getitem__(self, key):
        """Get the value corresponding to the key.
        Raise a KeyError if no such key found.
        """
        if self._root is None:
            raise KeyError('empty tree')
        else:
            return self._root.getitem(key).value

    def __setitem__(self, key, value):
        """Set self[key] to be value.
        Overwrite the old value if key found.
        """
        if self._root is None:
            self._root = _BinaryNode(key, value)
        else:
            self._root = self._root.setitem(key, value)

    def __delitem__(self, key):
        """Delete self[key].
        Raise a KeyError if no such key found.
        """
        if self._root is None:
            raise KeyError('empty tree')
        else:
            self._root = self._root.delitem(key)


class _BinaryNode:
    """Represent a binary tree node that stores an item.
    Methods in this class operate on and return other _BinaryNode objects.
    """
    __slots__ = 'key', 'value', 'left', 'right', 'length'

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.length = 1

    def __iter__(self):
        """An inorder traversal over child nodes"""
        if self.left is not None:
            yield from self.left
        yield self
        if self.right is not None:
            yield from self.right

    """Ordering methods"""

    def minimum(self):
        """Return the node with the minimum key"""
        if self.left is None:
            return self
        else:
            return self.left.minimum()

    def maximum(self):
        """Return the node with the maximum key"""
        if self.right is None:
            return self
        else:
            return self.right.maximum()

    def predecessor(self, key):
        """Return the node with the largest key that is strictly less than the given key.
        Raise a KeyError if no such node found.
        """
        if key <= self.key:
            # the predecessor is in the left branch
            if self.left is None:
                raise KeyError(f'No key less than {key}')
            else:
                return self.left.predecessor(key)

        elif self.right is None:
            # no key greater than self.key
            return self

        else:
            # if the predecessor can't be found in the right branch,
            # no key in the right branch is less than the given key
            try:
                return self.right.predecessor(key)
            except KeyError:
                return self

    def successor(self, key):
        """Return the node with the smallest key that is strictly greater than the given key.
        Raise a KeyError if no such node found.
        """
        # the logic is similar to finding the predecessor
        if key >= self.key:
            if self.right is None:
                raise KeyError(f'No key greater than {key}')
            else:
                return self.right.successor(key)

        elif self.left is None:
            return self

        else:
            try:
                return self.left.successor(key)
            except KeyError:
                return self

    """Accessor methods"""

    def getitem(self, key):
        """Do a recursive binary search to find the key and return the corresponding node.
        Raise a KeyError if no such node found.
        """
        if key == self.key:
            return self
        elif key < self.key and self.left is not None:
            return self.left.getitem(key)
        elif key > self.key and self.right is not None:
            return self.right.getitem(key)
        else:
            raise KeyError(f'key {key} not found')

    def setitem(self, key, value):
        """Find the correct position to either insert a new node with given key or
        overwrite the value of an existing node.
        Return the modified node.
        """
        if key == self.key:
            self.value = value

        elif key < self.key:
            # if the node has no left child, create new node
            # otherwise, recursively call setitem on left child
            # update length based on the change of left child's length
            if self.left is None:
                self.left = _BinaryNode(key, value)
                self.length += 1
            else:
                old_left_len = self.left.length
                self.left = self.left.setitem(key, value)
                self.length += self.left.length - old_left_len

        else:
            # similar to above, delegate to right child
            if self.right is None:
                self.right = _BinaryNode(key, value)
                self.length += 1
            else:
                old_right_len = self.right.length
                self.right = self.right.setitem(key, value)
                self.length += self.right.length - old_right_len

        return self

    def delitem(self, key):
        """Find the key and delete the corresponding node.
        Return the modified node, or raise a KeyError if no such node found.
        """
        if key == self.key:
            # if the node has no child, simply return None
            # if only one child, promote that child
            if self.left is None:
                return self.right
            elif self.right is None:
                return self.left

            # if the node has two children, replace it by its predecessor
            # (slight bias in favour of cutting the left branch)
            else:
                pred_node = self.predecessor(key)
                self.key = pred_node.key
                self.value = pred_node.value
                self.length -= 1

                # recursively call delitem on left child
                # the call would eventually reach pred_node and delete it
                # pred_node has only one or no child
                self.left = self.left.delitem(self.key)
                return self

        elif key < self.key and self.left is not None:
            # if calling delitem on left child didn't raise a KeyError,
            # that means exactly one descendant has been deleted
            try:
                self.left = self.left.delitem(key)
            except KeyError:
                raise
            else:
                self.length -= 1
                return self

        elif key > self.key and self.right is not None:
            # similar to above, try calling delitem on right child
            try:
                self.right = self.right.delitem(key)
            except KeyError:
                raise
            else:
                self.length -= 1
                return self

        else:
            raise KeyError(f'key {key} not found')
