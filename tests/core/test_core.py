from terragraph.core import Terragraph

GRAPH_STRING_EDGES = 25
GRAPH_STRING_NODES = 7


def test_get_edges(graph_string):
    """
    Tests the graph_string example has the expected number of edges
    :param graph_string:
    :return:
    """
    tg = Terragraph(dot_data=graph_string)
    assert len(tg.get_edges()) == GRAPH_STRING_EDGES


def test_get_nodes(graph_string):
    """
    Tests the graph_string example has the expected number of nodes
    :param graph_string:
    :return:
    """
    tg = Terragraph(dot_data=graph_string)
    assert len(tg.get_nodes()) == GRAPH_STRING_NODES
