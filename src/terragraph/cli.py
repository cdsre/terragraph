#!/usr/bin/env python
"""Console script for terragraph."""
import sys
import click

from terragraph.core import HighlightingMode, create_highlighted_svg, from_file


@click.group()
def terragraph():
    """Console script for terragraph."""


@terragraph.command()
@click.option('--file-name', required=True, type=click.Path(exists=True, dir_okay=False))
@click.option('--node-name', required=True, help="Name of the node to highlight")
@click.option('--mode', type=click.Choice([e.value for e in HighlightingMode]),
              default=HighlightingMode.PRECEDING.value, help='Select highlighting mode')
def highlight(file_name: str, node_name: str, mode: HighlightingMode):
    """
    Highlights a node and its edges
    """
    if file_name:
        create_highlighted_svg(file_name, node_name, mode=HighlightingMode(mode))
    return 0


@terragraph.command()
@click.option('--file-name', required=True, type=click.Path(exists=True, dir_okay=False))
def show_nodes(file_name: str):
    """
    Lists nodes in the terraform graph
    """
    print(f"file is: {file_name}")
    tfg = from_file(file_name)
    for node in tfg.get_node_names():
        print(node)

if __name__ == "__main__":
    sys.exit(terragraph())  # pragma: no cover
