import abc
from collections import namedtuple

from heap_queue import HeapQueue
from partition import Partition

DirectedEdge = namedtuple('DirectedEdge', 'start end weight')
Edge = namedtuple('Edge', 'pair weight')

INF = float('inf')


class WeightedGraph(abc.ABC):
    """An abstract base class for a weighted graph."""

    @abc.abstractmethod
    def add_node(self, label):
        """Add a node with the given label.
        No effect if a node with the given label already exists.
        """

    @abc.abstractmethod
    def add_edge(self, start, end, weight):
        """Add an edge from start to end with the given weight.
        Add the nodes automatically if not already exist.
        Overwrite the weight if the edge already exists.
        """

    @abc.abstractmethod
    def remove_node(self, label):
        """Remove the node with the given label.
        Remove all edges at the node automatically.
        Raise a ValueError if the node does not exist.
        """

    @abc.abstractmethod
    def remove_edge(self, start, end):
        """Remove the edge from start to end.
        Raise a ValueError if the edge does not exist
        """

    @property
    @abc.abstractmethod
    def nodes(self):
        """Return an iterator over all nodes."""

    @property
    @abc.abstractmethod
    def edges(self):
        """Return an iterator over all edges."""

    @property
    @abc.abstractmethod
    def node_count(self):
        """Return the number of nodes."""

    @property
    @abc.abstractmethod
    def edge_count(self):
        """Return the number of edges."""

    @abc.abstractmethod
    def neighbors(self, label):
        """Return an iterator, in which each item is an (neighbor, weight) pair,
        where neighbor is an out-neighbor of the node with the given label and
        weight is the weight of the corresponding edge.
        Raise a ValueError if the node does not exist.
        """

    @abc.abstractmethod
    def degree(self, label):
        """Return the (out-)degree of the node with the given label.
        Raise a ValueError if the node does not exist.
        """

    @abc.abstractmethod
    def weight(self, start, end):
        """Return the weight of the edge from start to end.
        Raise a ValueError if the edge does not exist.
        """


class DirectedGraph(WeightedGraph):
    """Implement a directed weighted graph using adjacency map."""

    def __init__(self):
        """Initialize the graph with an adjacency map."""
        self._adjacency = {}

    def add_node(self, label):
        # if no such node, initialize the corresponding neighbour dict
        self._adjacency.setdefault(label, {})

    def add_edge(self, start, end, weight):
        self._adjacency.setdefault(end, {})

        # extract the neighbour dict of start and set weight
        nbr_dict = self._adjacency.setdefault(start, {})
        nbr_dict[end] = weight

    def remove_node(self, label):
        if label not in self._adjacency:
            raise ValueError(f'no node {label}')

        else:
            del self._adjacency[label]

            # delete all edges whose end node is the given node
            for _, nbr_dict in self._adjacency.items():
                nbr_dict.pop(label, None)

    def remove_edge(self, start, end):
        try:
            del self._adjacency[start][end]

        # Two cases result in a KeyError
        # Case 1: start node does not exist, or
        # Case 2: start node exists but no edge from it to the end node
        except KeyError:
            raise ValueError(f'no edge from {start} to {end}')

    @property
    def nodes(self):
        yield from self._adjacency

    @property
    def edges(self):
        """Iterate over all edges. Each edge is represented as a namedtuple
        of the form DirectedEdge(start, end, weight).
        """
        for start, nbr_dict in self._adjacency.items():
            for end, weight in nbr_dict.items():
                yield DirectedEdge(start, end, weight)

    @property
    def node_count(self):
        return len(self._adjacency)

    @property
    def edge_count(self):
        return sum(len(nbr_dict) for nbr_dict in self._adjacency.values())

    def neighbors(self, label):
        if label not in self._adjacency:
            raise ValueError(f'no node {label}')

        # return iter instead of yield from, otherwise ValueError is never
        # raised upon the initialization of the generator
        else:
            nbr_dict = self._adjacency[label]
            return iter(nbr_dict.items())

    def degree(self, label):
        if label not in self._adjacency:
            raise ValueError(f'no node {label}')
        else:
            return len(self._adjacency[label])

    def weight(self, start, end):
        try:
            return self._adjacency[start][end]

        # similar to remove_edge, two cases result in a KeyError
        except KeyError:
            raise ValueError(f'no edge from {start} to {end}')

    def single_source_shortest_paths(self, start, targets):
        """Find the shortest paths to multiple targets from a single source.
        Return a dictionary whose keys are the given targets and values are the
        corresponding shortest paths.
        """
        targets = list(targets)

        # check all nodes exist
        if start not in self._adjacency:
            raise ValueError(f'no node {start}')
        for target in targets:
            if target not in self._adjacency:
                raise ValueError(f'no node {target}')

        # use dijkstra to obtain the shortest-path tree, which
        # is then used to construct a path for each target
        result = {}
        came_from = self._dijkstra(start, targets)

        for target in targets:
            if target not in came_from:
                # no path from start to target
                path = []
            else:
                path = DirectedGraph._construct_path(came_from, target)
            result[target] = path

        return result

    def _dijkstra(self, start, targets):
        """A helper method that implements the Dijkstra algorithm.
        Return the shortest-path tree represented as a dict came_from.
        """
        came_from = {start: None}
        targets = set(targets)

        # initialize the cost of every node to be infinity, except the start
        frontier = HeapQueue((node, INF) for node in self.nodes)
        frontier.push(start, 0)

        while frontier:
            # node popped from the queue already has its shortest path found,
            # can be safely discarded
            cur_node, cur_cost = frontier.pop()
            targets.discard(cur_node)

            # if all targets are found, stop
            if not targets:
                break

            for nxt_node, weight in self.neighbors(cur_node):
                # only relax the nodes to which shortest paths are not yet found
                if nxt_node in frontier:
                    nxt_cost = cur_cost + weight

                    # if new cost less than the current cost, update it
                    if nxt_cost < frontier[nxt_node]:
                        frontier.push(nxt_node, nxt_cost)
                        came_from[nxt_node] = cur_node

        return came_from

    @staticmethod
    def _construct_path(came_from, target):
        """Given the shortest-path tree came_from,
        find the path from start to the given target.
        """
        cur_node = target
        path = []

        # backtrack from target until hitting the beginning
        while cur_node is not None:
            path.append(cur_node)
            cur_node = came_from[cur_node]

        # the path is in the reversed order
        path.reverse()
        return path


class EdgeMapGraph(WeightedGraph):
    """Implement an undirected weighted graph using edge map."""

    def __init__(self):
        """Initialize the graph with a node set and an edge map."""
        self._nodes = set()
        self._edges = {}

    def add_node(self, label):
        self._nodes.add(label)

    def add_edge(self, start, end, weight):
        self._nodes.add(start)
        self._nodes.add(end)
        pair = frozenset({start, end})
        self._edges[pair] = weight

    def remove_node(self, label):
        if label not in self._nodes:
            raise ValueError(f'no node {label}')
        else:
            self._nodes.remove(label)
            # retain edges that don't contain the given node
            self._edges = {pair: weight for pair, weight in self._edges.items()
                           if label not in pair}

    def remove_edge(self, start, end):
        pair = frozenset({start, end})
        if pair not in self._edges:
            raise ValueError(f'no edge from {start} to {end}')
        else:
            del self._edges[pair]

    @property
    def nodes(self):
        yield from self._nodes

    @property
    def edges(self):
        for pair, weight in self._edges.items():
            yield Edge(pair, weight)
    
    @property
    def node_count(self):
        return len(self._nodes)

    @property
    def edge_count(self):
        return len(self._edges)

    def neighbors(self, label):
        if label not in self._nodes:
            raise ValueError(f'no node {label}')

        # return a generator instead of yield from so that
        # ValueError is raised correctly
        else:
            return self._gen_nbrs(label)

    def _gen_nbrs(self, label):
        # helper method to generate the neighbors
        for (start, end), weight in self._edges.items():
            if start == label:
                yield (end, weight)
            elif end == label:
                yield (start, weight)

    def degree(self, label):
        if label not in self._nodes:
            raise ValueError(f'no node {label}')
        else:
            return sum(label in pair for pair in self._edges)

    def weight(self, start, end):
        pair = frozenset({start, end})
        if pair not in self._edges:
            raise ValueError(f'no edge from {start} to {end}')
        else:
            return self._edges[pair]

    @property
    def min_span_tree(self):
        """Use the Kruskal's algorithm to find the minimum spanning tree."""
        result = []
        forest = Partition(self.nodes)

        # greedily pick lighter edges first
        sorted_edges = sorted(self.edges, key=lambda edge: edge.weight)

        for edge in sorted_edges:
            start, end = edge.pair

            # Add the edge to the tree if its nodes belong to different groups
            if forest.find(start) != forest.find(end):
                result.append(edge)
                forest.union(start, end)

            # the mst must have (self.node_count - 1) edges
            if len(result) == self.node_count - 1:
                break

        return result
