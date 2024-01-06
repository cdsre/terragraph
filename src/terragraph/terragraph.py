"""Main module."""
import pydot
from enum import Enum


class HighlightingMode(Enum):
    ALL = "ALL"
    PRECEDING = "PRECEDING"
    SUCCESSOR = "SUCCESSOR"


DEFAULT_HIGHLIGHTING_MODE = HighlightingMode.PRECEDING


def get_graph_from_file(filename: str) -> pydot.Graph:
    # Your DOT input
    with open(filename) as dot_file:
        dot_input = dot_file.read()
        return pydot.graph_from_dot_data(dot_input)[0]


def get_preceding_edges(graph: pydot.Graph, edges: list[pydot.Edge]) -> list[pydot.Edge]:
    destination_edge_names: list[pydot.Edge] = [edge.get_destination() for edge in edges]

    if destination_edge_names:
        destination_edges: list[pydot.Edge] = [edge for edge in graph.get_edges() if
                                               edge.get_source() in destination_edge_names]
        return destination_edges + get_preceding_edges(graph, destination_edges)
    return []


def get_successor_edges(graph: pydot.Graph, edges: list[pydot.Edge]) -> list[pydot.Edge]:
    successor_edge_names: list[pydot.Edge] = [edge.get_source() for edge in edges]

    if successor_edge_names:
        successor_edges: list[pydot.Edge] = [edge for edge in graph.get_edges() if
                                             edge.get_destination() in successor_edge_names]
        return successor_edges + get_successor_edges(graph, successor_edges)
    return []


def highlight_node(graph: pydot.Graph, node_name: str, color="red", mode=DEFAULT_HIGHLIGHTING_MODE) -> None:
    node = graph.get_node(node_name)[0]
    node.set_color(color)
    highlight_node_edges(graph, node_name, mode=mode)


def highlight_edges(edges: list[pydot.Edge], color="red") -> None:
    for edge in edges:
        edge.set_color(color)


def get_all_preceding_edges(graph: pydot.Graph, node_name: str) -> list[pydot.Edge]:
    node_preceding_edges = [edge for edge in graph.get_edges() if edge.get_source() == node_name]
    preceding_edges = get_preceding_edges(graph, node_preceding_edges)
    return node_preceding_edges + preceding_edges


def get_all_successor_edges(graph: pydot.Graph, node_name: str) -> list[pydot.Edge]:
    node_successor_edges = [edge for edge in graph.get_edges() if edge.get_destination() == node_name]
    successor_edges = get_successor_edges(graph, node_successor_edges)
    return node_successor_edges + successor_edges


def highlight_node_edges(graph: pydot.Graph, node_name: str, mode=DEFAULT_HIGHLIGHTING_MODE) -> None:
    edges: list[pydot.Edge] = []
    if mode in [HighlightingMode.PRECEDING, HighlightingMode.ALL]:
        edges += get_all_preceding_edges(graph, node_name)
    if mode in [HighlightingMode.SUCCESSOR, HighlightingMode.ALL]:
        edges += get_all_successor_edges(graph, node_name)
    highlight_edges(edges)


def create_highlighted_svg(dot_file_name: str, highlighted_node_name: str, mode=DEFAULT_HIGHLIGHTING_MODE) -> None:
    graph = get_graph_from_file(dot_file_name)
    subgraph = graph.get_subgraph('"root"')[0]
    highlight_node(subgraph, highlighted_node_name, mode=mode)

    # Output the SVG file
    output_file_path = f"{dot_file_name}.svg"
    graph.write(output_file_path, format="svg")

    print(f"Colored node SVG file generated: {output_file_path}")


def get_nodes_list(dot_file_name: str) -> list[str]:
    graph = get_graph_from_file(dot_file_name)
    subgraph = graph.get_subgraph('"root"')[0]
    return [node.get_name() for node in subgraph.get_nodes()]
