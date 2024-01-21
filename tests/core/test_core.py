"""
A collection of tests for the core module
"""
import pytest

from terragraph.core import HighlightingMode, Terragraph

GRAPH_STRING_EDGES = 25
GRAPH_STRING_NODES = 7


def test_get_edges(terragraph_example):
    """
    Tests the terragraph_example example has the expected number of edges
    :param graph_string:
    :return:
    """
    assert len(terragraph_example.get_edges()) == GRAPH_STRING_EDGES


def test_get_nodes(terragraph_example):
    """
    Tests the terragraph_example example has the expected number of nodes
    :param graph_string:
    :return:
    """
    assert len(terragraph_example.get_nodes()) == GRAPH_STRING_NODES


def test_get_highlighted_nodes(terragraph_example):
    """
    Passes a node to be highlighted and checks its highlighted nodes
    :param terragraph_example:
    :return:
    """
    terragraph_example.highlight_node('"[root] module.mod1.random_pet.this2 (expand)"')
    assert len(terragraph_example.get_highlighted_nodes()) == 1


@pytest.mark.parametrize(
    ("node", "mode", "num_edges"),
    [
        (
            '"[root] module.mod1.random_pet.this2 (expand)"',
            HighlightingMode.SUCCESSOR,
            4,
        ),
        (
            '"[root] module.mod1.random_pet.this2 (expand)"',
            HighlightingMode.PRECEDING,
            7,
        ),
        ('"[root] module.mod1.random_pet.this2 (expand)"', HighlightingMode.ALL, 11),
    ],
)
def test_get_highlighted_edges(node, mode, num_edges, graph_string):
    """
    Passes a node to be highlighted and checks its highlighted edges
    :param terragraph_example:
    :return:
    """
    terragraph_example = Terragraph(dot_data=graph_string, highlighting_mode=mode)
    terragraph_example.highlight_node(node)
    assert len(terragraph_example.get_highlighted_edges()) == num_edges
