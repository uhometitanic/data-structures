class Partition:
    """Implement a partition of a set of items to disjoint subsets (groups) as
    a forest of trees, in which each tree represents a separate group.
    Two trees represent the same group if and only if they have the same root.
    Support union operation of two groups.
    """

    def __init__(self, items):
        items = list(items)

        # parents of every node in the forest
        self._parents = {item: item for item in items}

        # the sizes of the subtree
        self._weights = {item: 1 for item in items}

    def __len__(self):
        return len(self._parents)

    def __contains__(self, item):
        return item in self._parents

    def __iter__(self):
        yield from self._parents

    def add_item(self, item):
        """Add an item as a singleton group, if the item does not already exist
        in the partition.
        """
        if item not in self:
            self._parents[item] = item
            self._weights[item] = 1

    def add_group(self, items):
        """Add a list of items to form a separate group.
        Raise a ValueError if any item already exists in the partition.
        """
        items = list(items)
        for item in items:
            if item in self:
                raise ValueError(f"{item} already exists")

        # make the flattest tree possible, in which
        # the root is the parents of all other nodes
        # we choose item[0] to be the root
        self._parents[items[0]] = items[0]
        self._weights[items[0]] = len(items)
        for item in items[1:]:
            self._parents[item] = items[0]
            self._weights[item] = 1

    def find(self, item):
        """Return the root of the group containing the given item.
        Also reset the parents of all nodes along the path to the root.
        """
        if self._parents[item] == item:
            return item
        else:
            # find the root and recursively set all parents to it
            root = self.find(self._parents[item])
            self._parents[item] = root
            return root

    def union(self, item1, item2):
        """Merge the two groups (if they are disjoint) containing
        the two given items.
        """
        root1 = self.find(item1)
        root2 = self.find(item2)

        if root1 != root2:
            if self._weights[root1] < self._weights[root2]:
                # swap two roots so that root1 becomes heavier
                root1, root2 = root2, root1

            # root1 is heavier, reset parent of root2 to root1
            # also update the weight of the tree at root1
            self._parents[root2] = root1
            self._weights[root1] += self._weights[root2]

    @property
    def is_single_group(self):
        """Return true if all items are contained in a single group."""
        # we just need one item, any item is ok
        item = next(iter(self))

        # group size is the weight of the root
        group_size = self._weights[self.find(item)]
        return group_size == len(self)


if __name__ == '__main__':
    """We do tests here instead of unit tests,
    since the partition structure is quite simple.
    """
    p = Partition(range(10))

    p.union(3, 4)
    p.union(4, 9)
    p.union(8, 0)
    expected = {0: 8, 1: 1, 2: 2, 3: 3, 4: 3, 5: 5, 6: 6, 7: 7, 8: 8, 9: 3}
    print(p._parents)
    print('p._parents == expected?', p._parents == expected)
    print('p.is_single_group?', p.is_single_group)
    print()

    p.union(2, 3)
    p.union(5, 6)
    p.union(5, 9)
    expected = {0: 8, 1: 1, 2: 3, 3: 3, 4: 3, 5: 3, 6: 5, 7: 7, 8: 8, 9: 3}
    print(p._parents)
    print('p._parents == expected?', p._parents == expected)
    print('p.is_single_group?', p.is_single_group)
    print()

    p.union(7, 3)
    p.union(4, 8)
    p.union(6, 1)
    expected = {0: 8, 1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3}
    print(p._parents)
    print('p._parents == expected?', p._parents == expected)
    print('p.is_single_group?', p.is_single_group)
    print()

    p.add_group(range(10, 15))
    expected_parents = {0: 8, 1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3,
                        10: 10, 11: 10, 12: 10, 13: 10, 14: 10}
    print(p._parents)
    print('p._parents == expected?', p._parents == expected_parents)
    print('p._weights:')
    print(p._weights)
    print('p.is_single_group?', p.is_single_group)
    print()
