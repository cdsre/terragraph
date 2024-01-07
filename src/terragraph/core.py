"""
The core of the terragraph module
"""
from enum import Enum
import pydot  # type: ignore


class HighlightingMode(Enum):
    """
    An Enum for managing the highlighting modes for edges
    """

    ALL = "all"
    PRECEDING = "preceding"
    SUCCESSOR = "successor"


class Terragraph:
    """
    A class that will parse the output from a `terraform graph` command and can highlight a node and its associated edges.
    It can highlight preceeding edges, or succesor edges. It can also highlight both allowing the full dependency tree
    top and bottom for a given node.
    """

    DEFAULT_HIGHLIGHTING_MODE = HighlightingMode.PRECEDING

    def __init__(
        self,
        dot_data: str,
        subgraph_name: str = '"root"',
        highlighting_mode: HighlightingMode = DEFAULT_HIGHLIGHTING_MODE,
    ):
        self.__graph = pydot.graph_from_dot_data(dot_data)[0]
        self.tf_graph = self.__graph.get_subgraph(subgraph_name)[0]
        self.highlight_mode = highlighting_mode

    def __get_preceding_edges(self, edges: list[pydot.Edge]) -> list[pydot.Edge]:
        destination_edge_names: list[pydot.Edge] = [
            edge.get_destination() for edge in edges
        ]

        if destination_edge_names:
            destination_edges: list[pydot.Edge] = [
                edge
                for edge in self.tf_graph.get_edges()
                if edge.get_source() in destination_edge_names
            ]
            return destination_edges + self.__get_preceding_edges(destination_edges)
        return []

    def __get_successor_edges(self, edges: list[pydot.Edge]) -> list[pydot.Edge]:
        successor_edge_names: list[pydot.Edge] = [edge.get_source() for edge in edges]

        if successor_edge_names:
            successor_edges: list[pydot.Edge] = [
                edge
                for edge in self.tf_graph.get_edges()
                if edge.get_destination() in successor_edge_names
            ]
            return successor_edges + self.__get_successor_edges(successor_edges)
        return []

    def highlight_node(self, node_name: str, color: str = "red") -> None:
        """
        Highlights a node and its given edges
        :param node_name: The name of the node to highlight from
        :param color: The color to highlight the node
        :return: None
        """
        node = self.tf_graph.get_node(node_name)[0]
        node.set_color(color)
        self.highlight_node_edges(node_name)

    @staticmethod
    def highlight_edges(edges: list[pydot.Edge], color: str = "red") -> None:
        """
        highlights a list of edges with the color name
        :param edges: A list of edge objects to be highlighted
        :param color: The color to highlight the edges
        :return: None
        """
        for edge in edges:
            edge.set_color(color)

    def __get_all_preceding_edges(self, node_name: str) -> list[pydot.Edge]:
        node_preceding_edges = [
            edge for edge in self.tf_graph.get_edges() if edge.get_source() == node_name
        ]
        preceding_edges = self.__get_preceding_edges(node_preceding_edges)
        return node_preceding_edges + preceding_edges

    def __get_all_successor_edges(self, node_name: str) -> list[pydot.Edge]:
        node_successor_edges = [
            edge
            for edge in self.tf_graph.get_edges()
            if edge.get_destination() == node_name
        ]
        successor_edges = self.__get_successor_edges(node_successor_edges)
        return node_successor_edges + successor_edges

    def highlight_node_edges(self, node_name: str) -> None:
        """
        Takes a node name and will highlight the node and its edges based on the self.highlight_mode value
        :param node_name: The name of the node to highlight and the edges from it.
        :return: None
        """
        edges: list[pydot.Edge] = []
        if self.highlight_mode in [HighlightingMode.PRECEDING, HighlightingMode.ALL]:
            edges += self.__get_all_preceding_edges(node_name)
        if self.highlight_mode in [HighlightingMode.SUCCESSOR, HighlightingMode.ALL]:
            edges += self.__get_all_successor_edges(node_name)
        self.highlight_edges(edges)

    def get_node_names(self) -> list[str]:
        """
        Gets a list of all the nodes in the terraform_graph
        :return: list of node names
        """
        return [node.get_name() for node in self.tf_graph.get_nodes()]

    def write_svg(self, file_name: str) -> None:
        """
        Write an SVG of the current graph state
        :param file_name: output file name
        :return: None
        """
        self.__graph.write(file_name, format="svg")


def create_highlighted_svg(
    dot_file_name: str,
    highlighted_node_name: str,
    mode: HighlightingMode = Terragraph.DEFAULT_HIGHLIGHTING_MODE,
) -> None:
    """
    Will create a highlighted representation of the graph under the same path as the dot_file_name but suffixed with .svg

    :param dot_file_name: The name/path to a file containing a terraform graph output
    :param highlighted_node_name: The node name to highlight in the graph and its edges.
    :param mode: An Enum indicating which highlighting mode to use
    :return: This does not return anything as it will create the SVG in the file system.
    """
    terragraph = from_file(dot_file_name, mode)
    terragraph.highlight_node(highlighted_node_name)

    # Output the SVG file
    output_file_path = f"{dot_file_name}.svg"
    terragraph.write_svg(output_file_path)

    print(f"Colored node SVG file generated: {output_file_path}")


def from_file(filename: str, mode: HighlightingMode = Terragraph.DEFAULT_HIGHLIGHTING_MODE) -> Terragraph:
    "Takes a file name containing a 'terraform graph' output and returns a Terragraph object of it"
    with open(filename, encoding="utf-8") as dot_file:
        dot_input = dot_file.read()
        return Terragraph(dot_input, highlighting_mode=mode)
