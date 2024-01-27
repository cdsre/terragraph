"""
A collection of tests for the core module
"""
import re

import pytest

from terragraph.core import HighlightingMode, Terragraph

GRAPH_STRING_EDGES = 25
GRAPH_STRING_NODES = 7
NODE1_NAME = '"[root] module.mod1.random_pet.this2 (expand)"'
NODE2_NAME = '"[root] module.mod2.random_pet.this (expand)"'
INVALID_NODE_NAME = '[root] module.invalid.random_pet.this (expand)"'


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


def test_highlight_node(terragraph_example):
    """
    Passes a node to be highlighted and checks its highlighted nodes
    :param terragraph_example:
    :return:
    """
    terragraph_example.highlight_node(NODE1_NAME)
    assert len(terragraph_example.get_highlighted_nodes()) == 1


def test_highlight_node_invalid_node_name(terragraph_example):
    """
    Tests that when an invalid node name is passed the method raises a value error
    :param terragraph_example:
    :return:
    """
    with pytest.raises(
        ValueError,
        match=f"Node '{re.escape(INVALID_NODE_NAME)}' is not a valid node in the graph",
    ):
        terragraph_example.highlight_node(INVALID_NODE_NAME)


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


def test_highlight_node_edges_invalid_node_name(graph_string):
    """
    Test that when using an invalid node name to highlight edges we get a ValueError
    :param graph_string:
    :return:
    """
    terragraph_example = Terragraph(dot_data=graph_string)
    with pytest.raises(
        ValueError,
        match=f"Node '{re.escape(INVALID_NODE_NAME)}' is not a valid node in the graph",
    ):
        terragraph_example.highlight_node_edges(INVALID_NODE_NAME)


def test_remove_unhighlighted_edges(terragraph_example):
    node_name = NODE2_NAME
    terragraph_example.highlight_node_edges(node_name)
    terragraph_example.remove_unhighlighted_elements()

    assert len(terragraph_example.get_nodes()) == 4
    assert len(terragraph_example.get_edges()) == 8
