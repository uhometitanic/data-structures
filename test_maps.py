import collections
import random
from string import ascii_lowercase
from itertools import product

import pytest
from hash_table import HashTable
from sorted_list_map import SortedListMap
from binary_search_tree import BinarySearchTree

"""Map Classes that we are testing."""

UNSORTED_MAPS = [HashTable, SortedListMap, BinarySearchTree]
SORTED_MAPS = [SortedListMap, BinarySearchTree]


"""Constants and a fixture for testing small fixed inputs.
The keys are deliberately repeated to test whether the maps contain repeated keys.
"""

KEYS = 'TU5AVERNIEH3WXBQ7AFOIIC20HP18AWSRDKRMSZUL46J9FLYG9'

KEY_SET = set(KEYS)
SORTED_KEYS = sorted(KEY_SET)
ITEMS = [(key, i) for i, key in enumerate(KEYS)]
DICT_ITEMS = dict(ITEMS).items()
SORTED_ITEMS = sorted(DICT_ITEMS)


@pytest.fixture(scope='class')
def fixed_input_map(request):
    """Return a map of the requested map class with the given fixed items."""
    my_map = request.param(ITEMS)
    return my_map


"""Constants, fixtures and helper functions for testing large random inputs.
The keys are drawn at random from the list of all strings of 3 lowercase letters.
"""

KEY_LEN = 3
POSSIBLE_KEYS = [''.join(chars) for chars in product(ascii_lowercase,
                                                     repeat=KEY_LEN)]


@pytest.fixture(scope='class')
def map_pair(request):
    """Return a map of the requested map class and also a python dictionary.
    In the tests, we would compare our maps with the python dicts.
    Since the scope is 'class', this fixture actually return the same
    my_map and python_dict instances for every test within the same test class.
    This means all modifications to my_map and python_dict done by previous tests
    are carried over to later tests.
    """
    my_map = request.param()
    python_dict = {}
    return my_map, python_dict


def random_setitem(my_map, python_dict):
    """Helper function for adding random items into my_map and python_dict.
    Number of added items equals number of possible keys.
    But since there are repeated added keys, not all possible keys are added.
    """
    added_keys = random.choices(POSSIBLE_KEYS, k=len(POSSIBLE_KEYS))
    for i, key in enumerate(added_keys):
        my_map[key] = i
        python_dict[key] = i
    return my_map, python_dict


def random_delitem(my_map, python_dict):
    """Helper function for removing random items from my_map and python_dict.
    Number of removed items is chosen to be 2/3 of the existing items.
    """
    num_dels = len(python_dict) * 2 // 3
    removed_keys = random.sample(python_dict.keys(), k=num_dels)
    for key in removed_keys:
        del my_map[key]
        del python_dict[key]
    return my_map, python_dict


"""Test classes"""


@pytest.mark.parametrize('fixed_input_map', UNSORTED_MAPS, indirect=True)
class TestUnsortedMapFixedInput:
    """Test class for unsorted maps with small fixed inputs."""

    def test_len(self, fixed_input_map):
        """Test the __len__ method."""
        assert len(fixed_input_map) == len(KEY_SET)

    def test_iter(self, fixed_input_map):
        """Test the __iter__method.
        Since we don't care about the ordering, we cast the iterator into a set.
        """
        assert set(key for key in fixed_input_map) == KEY_SET

    @pytest.mark.parametrize('key, value', DICT_ITEMS)
    def test_getitem(self, fixed_input_map, key, value):
        """Test the __getitem__ method for all (key, value) pair."""
        assert fixed_input_map[key] == value

    @pytest.mark.parametrize('key', KEY_SET)
    def test_delitem(self, fixed_input_map, key):
        """Test the __delitem__ method for all keys. After deleting a key,
        getting and deleting the same key should raise a KeyError.
        """
        del fixed_input_map[key]
        with pytest.raises(KeyError):
            fixed_input_map[key]
        with pytest.raises(KeyError):
            del fixed_input_map[key]

    def test_empty(self, fixed_input_map):
        """After deleting all items, the map should be empty."""
        assert len(fixed_input_map) == 0


@pytest.mark.parametrize('map_pair', UNSORTED_MAPS, indirect=True)
class TestUnsortedMapRandomInput:
    """Test class for unsorted maps with large random inputs.
    We added a large number of random items to each map and assert that the length
    of the map and the set of items are correct, then we randomly remove 2/3 of
    the items and assert again. The process is repeated three times.
    """

    def test_first_setitem(self, map_pair):
        my_map, python_dict = random_setitem(*map_pair)
        assert len(my_map) == len(python_dict)
        assert set(my_map.items()) == set(python_dict.items())

    def test_first_delitem(self, map_pair):
        my_map, python_dict = random_delitem(*map_pair)
        assert len(my_map) == len(python_dict)
        assert set(my_map.items()) == set(python_dict.items())

    def test_second_setitem(self, map_pair):
        my_map, python_dict = random_setitem(*map_pair)
        assert len(my_map) == len(python_dict)
        assert set(my_map.items()) == set(python_dict.items())

    def test_second_delitem(self, map_pair):
        my_map, python_dict = random_delitem(*map_pair)
        assert len(my_map) == len(python_dict)
        assert set(my_map.items()) == set(python_dict.items())

    def test_third_setitem(self, map_pair):
        my_map, python_dict = random_setitem(*map_pair)
        assert len(my_map) == len(python_dict)
        assert set(my_map.items()) == set(python_dict.items())

    def test_third_delitem(self, map_pair):
        my_map, python_dict = random_delitem(*map_pair)
        assert len(my_map) == len(python_dict)
        assert set(my_map.items()) == set(python_dict.items())


@pytest.mark.parametrize('fixed_input_map', SORTED_MAPS, indirect=True)
class TestSortedMapFixedInput:
    """Test class for sorted maps with small fixed inputs."""

    def test_minimum(self, fixed_input_map):
        """Test the minimum method."""
        assert fixed_input_map.minimum() == SORTED_ITEMS[0]

    def test_maximum(self, fixed_input_map):
        """Test the maximum method."""
        assert fixed_input_map.maximum() == SORTED_ITEMS[-1]

    def test_no_predecessor(self, fixed_input_map):
        """Test the predecessor method for the smallest key,
        which results in a KeyError.
        """
        with pytest.raises(KeyError):
            fixed_input_map.predecessor(SORTED_KEYS[0])

    def test_no_successor(self, fixed_input_map):
        """Test the successor method for the largest key,
        which results in a KeyError.
        """
        with pytest.raises(KeyError):
            fixed_input_map.successor(SORTED_KEYS[-1])

    @pytest.mark.parametrize('key', SORTED_KEYS[1:])
    def test_predecessor_is_key(self, fixed_input_map, key):
        """Test the predecessor method for all but the smallest key."""
        prev_item = SORTED_ITEMS[SORTED_KEYS.index(key) - 1]
        assert fixed_input_map.predecessor(key) == prev_item

    @pytest.mark.parametrize('key', SORTED_KEYS[:-1])
    def test_successor_is_key(self, fixed_input_map, key):
        """Test the successor method for all but the largest key."""
        next_item = SORTED_ITEMS[SORTED_KEYS.index(key) + 1]
        assert fixed_input_map.successor(key) == next_item

    @pytest.mark.parametrize('key', ':;<=>?@')
    def test_predecessor_not_key(self, fixed_input_map, key):
        """Test the predecessor method for all but the smallest key."""
        pred_key, _ = fixed_input_map.predecessor(key)
        assert pred_key == '9'

    @pytest.mark.parametrize('key', ':;<=>?@')
    def test_successor_not_key(self, fixed_input_map, key):
        """Test the successor method for all but the largest key."""
        succ_key, _ = fixed_input_map.successor(key)
        assert succ_key == 'A'


@pytest.mark.parametrize('map_pair', SORTED_MAPS, indirect=True)
class TestSortedMapRandomInput:
    """Test class for sorted maps with large random inputs.
    Similar to TestUnsortedMapRandomInput, we randomly add and remove items
    three times, but we test whether the lists of keys are sorted instead.
    """

    def test_first_setitem(self, map_pair):
        my_map, python_dict = random_setitem(*map_pair)
        assert list(my_map) == sorted(python_dict)

    def test_first_delitem(self, map_pair):
        my_map, python_dict = random_delitem(*map_pair)
        assert list(my_map) == sorted(python_dict)

    def test_second_setitem(self, map_pair):
        my_map, python_dict = random_setitem(*map_pair)
        assert list(my_map) == sorted(python_dict)

    def test_second_delitem(self, map_pair):
        my_map, python_dict = random_delitem(*map_pair)
        assert list(my_map) == sorted(python_dict)

    def test_third_setitem(self, map_pair):
        my_map, python_dict = random_setitem(*map_pair)
        assert list(my_map) == sorted(python_dict)

    def test_third_delitem(self, map_pair):
        my_map, python_dict = random_delitem(*map_pair)
        assert list(my_map) == sorted(python_dict)
