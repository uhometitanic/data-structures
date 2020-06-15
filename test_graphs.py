import pytest
from weighted_graph import *


def init_graph(graph_type):
    g = graph_type()
    g.add_node(0)
    g.add_edge(1, 2, -100)
    g.add_edge(3, 4, -100)

    g.add_edge(2, 1, 1)
    g.add_edge(4, 3, 3)
    g.add_edge(1, 0, 1)
    g.add_edge(0, 2, 2)
    g.add_edge(1, 3, 4)
    g.add_edge(3, 2, 5)

    g.add_node(0)
    g.add_edge(1, 2, 3)
    g.add_edge(3, 4, 6)
    return g


def cut_graph(g):
    g.remove_node(0)
    g.remove_node(4)
    g.remove_edge(2, 1)


@pytest.fixture(scope='class')
def digraph_before():
    return init_graph(DirectedGraph)


@pytest.fixture(scope='class')
def digraph_after(digraph_before):
    g = digraph_before
    cut_graph(g)
    return g


@pytest.fixture(scope='class')
def edgegraph_before():
    return init_graph(EdgeMapGraph)


@pytest.fixture(scope='class')
def edgegraph_after(edgegraph_before):
    g = edgegraph_before
    cut_graph(g)
    return g


@pytest.fixture(scope='class')
def big_graph_for_dijkstra():
    g = DirectedGraph()
    g._adjacency = {0: {4: 2},
                    1: {0: 5, 2: 3, 4: 2},
                    2: {1: 8},
                    3: {2: 9, 10: 9},
                    4: {0: 9, 1: 4, 5: 1, 8: 4},
                    5: {1: 9, 6: 8, 8: 4},
                    6: {},
                    7: {0: 5, 8: 1},
                    8: {},
                    9: {8: 5},
                    10: {3: 2},
                    11: {8: 6, 12: 3, 14: 5},
                    12: {13: 6, 16: 4},
                    13: {9: 5, 16: 8},
                    14: {7: 3, 11: 5},
                    15: {11: 8, 16: 8},
                    16: {12: 5, 15: 7, 17: 2},
                    17: {10: 9}}
    return g


@pytest.fixture(scope='class')
def big_graph_for_kruskal():
    g = EdgeMapGraph()
    g.add_edge(0, 1, 5)
    g.add_edge(0, 2, 3)
    g.add_edge(0, 4, 4)
    g.add_edge(0, 7, 4)
    g.add_edge(0, 14, 9)
    g.add_edge(1, 5, 8)
    g.add_edge(2, 5, 6)
    g.add_edge(2, 6, 2)
    g.add_edge(3, 6, 3)
    g.add_edge(3, 10, 1)
    g.add_edge(3, 17, 7)
    g.add_edge(4, 5, 9)
    g.add_edge(4, 8, 2)
    g.add_edge(5, 6, 4)
    g.add_edge(5, 8, 2)
    g.add_edge(5, 9, 4)
    g.add_edge(6, 9, 9)
    g.add_edge(6, 10, 6)
    g.add_edge(7, 11, 8)
    g.add_edge(8, 9, 3)
    g.add_edge(8, 11, 5)
    g.add_edge(8, 12, 5)
    g.add_edge(9, 10, 2)
    g.add_edge(9, 12, 3)
    g.add_edge(9, 13, 1)
    g.add_edge(11, 14, 2)
    g.add_edge(11, 15, 6)
    g.add_edge(12, 16, 3)
    g.add_edge(13, 16, 3)
    g.add_edge(14, 15, 6)
    g.add_edge(15, 17, 3)
    g.add_edge(16, 17, 6)
    return g


class TestDigraphAbstract:
    def test_nodes_before(self, digraph_before):
        g = digraph_before
        assert set(g.nodes) == set(range(5))

    def test_edges_before(self, digraph_before):
        g = digraph_before
        edge_set = {DirectedEdge(1, 2, 3),
                    DirectedEdge(2, 1, 1),
                    DirectedEdge(3, 4, 6),
                    DirectedEdge(4, 3, 3),
                    DirectedEdge(1, 0, 1),
                    DirectedEdge(0, 2, 2),
                    DirectedEdge(1, 3, 4),
                    DirectedEdge(3, 2, 5)}
        assert set(g.edges) == edge_set

    def test_node_count_before(self, digraph_before):
        g = digraph_before
        assert g.node_count == 5

    def test_edge_count_before(self, digraph_before):
        g = digraph_before
        assert g.edge_count == 8

    @pytest.mark.parametrize('node, expected', [(0, {(2, 2)}),
                                                (1, {(0, 1), (2, 3), (3, 4)}),
                                                (2, {(1, 1)}),
                                                (3, {(2, 5), (4, 6)}),
                                                (4, {(3, 3)})])
    def test_neighbors(self, digraph_before, node, expected):
        neighbors = digraph_before.neighbors(node)
        assert set(neighbors) == expected

    @pytest.mark.parametrize('node, expected', [(0, 1),
                                                (1, 3),
                                                (2, 1),
                                                (3, 2),
                                                (4, 1)])
    def test_degree(self, digraph_before, node, expected):
        degree = digraph_before.degree(node)
        assert degree == expected

    @pytest.mark.parametrize('start, end, expected', [(1, 2, 3),
                                                      (2, 1, 1),
                                                      (3, 4, 6),
                                                      (4, 3, 3),
                                                      (1, 0, 1),
                                                      (0, 2, 2),
                                                      (1, 3, 4),
                                                      (3, 2, 5)])
    def test_weight(self, digraph_before, start, end, expected):
        weight = digraph_before.weight(start, end)
        assert weight == expected

    def test_nodes_after(self, digraph_after):
        g = digraph_after
        assert set(g.nodes) == {1, 2, 3}

    def test_edges_after(self, digraph_after):
        g = digraph_after
        edge_set = {DirectedEdge(1, 2, 3),
                    DirectedEdge(1, 3, 4),
                    DirectedEdge(3, 2, 5)}
        assert set(g.edges) == edge_set

    def test_node_count_after(self, digraph_after):
        g = digraph_after
        assert g.node_count == 3

    def test_edge_count_after(self, digraph_after):
        g = digraph_after
        assert g.edge_count == 3

    @pytest.mark.parametrize('node', [0, 4, 5] * 2)
    def test_remove_node_error(self, digraph_after, node):
        g = digraph_after
        with pytest.raises(ValueError):
            g.remove_node(node)

    @pytest.mark.parametrize('start, end', [(1, 0),
                                            (0, 2),
                                            (2, 1),
                                            (3, 4),
                                            (4, 3)] * 2)
    def test_remove_edge_error(self, digraph_after, start, end):
        g = digraph_after
        with pytest.raises(ValueError):
            g.remove_edge(start, end)

    @pytest.mark.parametrize('node', [0, 4, 5] * 2)
    def test_neighbors_error(self, digraph_after, node):
        g = digraph_after
        with pytest.raises(ValueError):
            g.neighbors(node)

    @pytest.mark.parametrize('node', [0, 4, 5] * 2)
    def test_degree_error(self, digraph_after, node):
        g = digraph_after
        with pytest.raises(ValueError):
            g.degree(node)

    @pytest.mark.parametrize('start, end', [(1, 0),
                                            (0, 2),
                                            (2, 1),
                                            (3, 4),
                                            (4, 3)] * 2)
    def test_weight_error(self, digraph_after, start, end):
        g = digraph_after
        with pytest.raises(ValueError):
            g.weight(start, end)


class TestEdgeGraphAbstract:
    def test_nodes_before(self, edgegraph_before):
        g = edgegraph_before
        assert set(g.nodes) == set(range(5))

    def test_edges_before(self, edgegraph_before):
        g = edgegraph_before
        edge_set = {Edge(frozenset({1, 2}), 3),
                    Edge(frozenset({4, 3}), 6),
                    Edge(frozenset({1, 0}), 1),
                    Edge(frozenset({0, 2}), 2),
                    Edge(frozenset({1, 3}), 4),
                    Edge(frozenset({3, 2}), 5)}
        assert set(g.edges) == edge_set

    def test_node_count_before(self, edgegraph_before):
        g = edgegraph_before
        assert g.node_count == 5

    def test_edge_count_before(self, edgegraph_before):
        g = edgegraph_before
        assert g.edge_count == 6

    @pytest.mark.parametrize('node, expected', [(0, {(1, 1), (2, 2)}),
                                                (1, {(0, 1), (2, 3), (3, 4)}),
                                                (2, {(0, 2), (1, 3), (3, 5)}),
                                                (3, {(1, 4), (2, 5), (4, 6)}),
                                                (4, {(3, 6)})])
    def test_neighbors(self, edgegraph_before, node, expected):
        neighbors = edgegraph_before.neighbors(node)
        assert set(neighbors) == expected

    @pytest.mark.parametrize('node, expected', [(0, 2),
                                                (1, 3),
                                                (2, 3),
                                                (3, 3),
                                                (4, 1)])
    def test_degree(self, edgegraph_before, node, expected):
        degree = edgegraph_before.degree(node)
        assert degree == expected

    @pytest.mark.parametrize('start, end, expected', [(1, 2, 3),
                                                      (4, 3, 6),
                                                      (1, 0, 1),
                                                      (0, 2, 2),
                                                      (1, 3, 4),
                                                      (3, 2, 5)])
    def test_weight(self, edgegraph_before, start, end, expected):
        weight = edgegraph_before.weight(start, end)
        assert weight == expected

    def test_nodes_after(self, edgegraph_after):
        g = edgegraph_after
        assert set(g.nodes) == {1, 2, 3}

    def test_edges_after(self, edgegraph_after):
        g = edgegraph_after
        edge_set = {Edge(frozenset({1, 3}), 4),
                    Edge(frozenset({3, 2}), 5)}
        assert set(g.edges) == edge_set

    def test_node_count_after(self, edgegraph_after):
        g = edgegraph_after
        assert g.node_count == 3

    def test_edge_count_after(self, edgegraph_after):
        g = edgegraph_after
        assert g.edge_count == 2

    @pytest.mark.parametrize('node', [0, 4, 5] * 2)
    def test_remove_node_error(self, edgegraph_after, node):
        g = edgegraph_after
        with pytest.raises(ValueError):
            g.remove_node(node)

    @pytest.mark.parametrize('start, end', [(1, 0),
                                            (0, 2),
                                            (2, 1),
                                            (3, 4),
                                            (4, 3)] * 2)
    def test_remove_edge_error(self, edgegraph_after, start, end):
        g = edgegraph_after
        with pytest.raises(ValueError):
            g.remove_edge(start, end)

    @pytest.mark.parametrize('node', [0, 4, 5] * 2)
    def test_neighbors_error(self, edgegraph_after, node):
        g = edgegraph_after
        with pytest.raises(ValueError):
            g.neighbors(node)

    @pytest.mark.parametrize('node', [0, 4, 5] * 2)
    def test_degree_error(self, edgegraph_after, node):
        g = edgegraph_after
        with pytest.raises(ValueError):
            g.degree(node)

    @pytest.mark.parametrize('start, end', [(1, 0),
                                            (0, 2),
                                            (2, 1),
                                            (3, 4),
                                            (4, 3)] * 2)
    def test_weight_error(self, edgegraph_after, start, end):
        g = edgegraph_after
        with pytest.raises(ValueError):
            g.weight(start, end)


class TestDigraphAlgorithm:
    def test_dijkstra_no_target(self, digraph_before):
        g = digraph_before
        paths = g.single_source_shortest_paths(0, [])
        expected_paths = {}
        assert paths == expected_paths

    def test_dijkstra_before_1(self, digraph_before):
        g = digraph_before
        paths = g.single_source_shortest_paths(1, range(5))
        expected_paths = {0: [1, 0],
                          1: [1],
                          2: [1, 2],
                          3: [1, 3],
                          4: [1, 3, 4]}
        assert paths == expected_paths

    def test_dijkstra_before_4(self, digraph_before):
        g = digraph_before
        paths = g.single_source_shortest_paths(4, range(5))
        expected_paths = {0: [4, 3, 2, 1, 0],
                          1: [4, 3, 2, 1],
                          2: [4, 3, 2,],
                          3: [4, 3],
                          4: [4]}
        assert paths == expected_paths

    def test_dijkstra_after_2(self, digraph_after):
        g = digraph_after
        paths = g.single_source_shortest_paths(2, [1, 2, 3])
        expected_paths = {1: [],
                          2: [2],
                          3: []}
        assert paths == expected_paths

    def test_dijkstra_after_3(self, digraph_after):
        g = digraph_after
        paths = g.single_source_shortest_paths(3, [1, 2, 3])
        expected_paths = {1: [],
                          2: [3, 2],
                          3: [3]}
        assert paths == expected_paths

    @pytest.mark.parametrize('start, targets', [(0, [1, 2]),
                                                (3, [0, 4]),
                                                (1, [2, 3, 4])])
    def test_dijkstra_error(self, digraph_after, start, targets):
        g = digraph_after
        with pytest.raises(ValueError):
            g.single_source_shortest_paths(start, targets)

    def test_dijkstra_big_graph_15(self, big_graph_for_dijkstra):
        g = big_graph_for_dijkstra
        paths = g.single_source_shortest_paths(15, [1, 6, 11, 16])
        expected_paths = {1: [15, 11, 14, 7, 0, 4, 1],
                          6: [15, 11, 14, 7, 0, 4, 5, 6],
                          11: [15, 11],
                          16: [15, 16]}
        assert paths == expected_paths

    def test_dijkstra_big_graph_17(self, big_graph_for_dijkstra):
        g = big_graph_for_dijkstra
        paths = g.single_source_shortest_paths(17, [1, 6, 11, 16])
        expected_paths = {1: [17, 10, 3, 2, 1],
                          6: [17, 10, 3, 2, 1, 4, 5, 6],
                          11: [],
                          16: []}
        assert paths == expected_paths


class TestEdgeGraphAlgorithm:
    def test_kruskal_single_node(self):
        g = EdgeMapGraph()
        g.add_node(0)
        mst = g.min_span_tree
        expected_mst = []
        assert mst == expected_mst

    def test_kruskal_before(self, edgegraph_before):
        g = edgegraph_before
        mst = g.min_span_tree
        expected_mst = [Edge(frozenset({1, 0}), 1),
                        Edge(frozenset({0, 2}), 2),
                        Edge(frozenset({1, 3}), 4),
                        Edge(frozenset({4, 3}), 6)]
        assert mst == expected_mst

    def test_kruskal_after(self, edgegraph_after):
        g = edgegraph_after
        mst = g.min_span_tree
        expected_mst = [Edge(frozenset({1, 3}), 4),
                        Edge(frozenset({3, 2}), 5)]
        assert mst == expected_mst

    def test_kruskal_big_graph(self, big_graph_for_kruskal):
        g = big_graph_for_kruskal
        mst = g.min_span_tree
        expected_mst = {Edge(frozenset({0, 1}), 5),
                        Edge(frozenset({0, 2}), 3),
                        Edge(frozenset({0, 7}), 4),
                        Edge(frozenset({2, 6}), 2),
                        Edge(frozenset({3, 6}), 3),
                        Edge(frozenset({3, 10}), 1),
                        Edge(frozenset({4, 8}), 2),
                        Edge(frozenset({5, 8}), 2),
                        Edge(frozenset({8, 9}), 3),
                        Edge(frozenset({8, 11}), 5),
                        Edge(frozenset({9, 10}), 2),
                        Edge(frozenset({9, 12}), 3),
                        Edge(frozenset({9, 13}), 1),
                        Edge(frozenset({11, 14}), 2),
                        Edge(frozenset({11, 15}), 6),
                        Edge(frozenset({12, 16}), 3),
                        Edge(frozenset({15, 17}), 3)}
        assert set(mst) == expected_mst
