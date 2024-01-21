"""
A collection of tests for the core module
"""
import pytest

from terragraph.core import HighlightingMode, Terragraph

GRAPH_STRING_EDGES = 25
GRAPH_STRING_NODES = 7
NODE1_NAME = '"[root] module.mod1.random_pet.this2 (expand)"'
NODE2_NAME = '"[root] module.mod2.random_pet.this (expand)"'


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


def test_highlighted_node(terragraph_example):
    """
    Passes a node to be highlighted and checks its highlighted nodes
    :param terragraph_example:
    :return:
    """
    terragraph_example.highlight_node('"[root] module.mod1.random_pet.this2 (expand)"')
    assert len(terragraph_example.get_highlighted_nodes()) == 1


@pytest.mark.parametrize(
    ("node_name", "highlight_mode", "expected_num_edges"),
    [
        (
            NODE1_NAME,
            HighlightingMode.SUCCESSOR,
            4,
        ),
        (
            NODE1_NAME,
            HighlightingMode.PRECEDING,
            7,
        ),
        (NODE1_NAME, HighlightingMode.ALL, 11),
        (
            NODE2_NAME,
            HighlightingMode.SUCCESSOR,
            4,
        ),
        (
            NODE2_NAME,
            HighlightingMode.PRECEDING,
            8,
        ),
        (NODE2_NAME, HighlightingMode.ALL, 12),
    ],
)
def test_highlight_node_edges(
    node_name, highlight_mode, expected_num_edges, graph_string
):
    """
    Will use a node it a Highlighting mode and test that the expected number of edges were highlighted
    :param node_name: The node name to highlight
    :param highlight_mode: The Highlighting mode
    :param expected_num_edges: The expected number of edges
    :param graph_string: The graph_string example
    :return:
    """
    terragraph_example = Terragraph(
        dot_data=graph_string, highlighting_mode=highlight_mode
    )
    terragraph_example.highlight_node_edges(node_name)
    assert len(terragraph_example.get_highlighted_edges()) == expected_num_edges
