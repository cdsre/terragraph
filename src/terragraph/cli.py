#!/usr/bin/env python
"""Console script for terragraph."""
import sys
import click

from .terragraph import HighlightingMode, create_highlighted_svg


@click.command()
@click.option('--file-name', type=click.Path(exists=True, dir_okay=False))
@click.option('--node-name', required=True, help="Name of the node to highlight")
@click.option('--mode', type=click.Choice([e.value for e in HighlightingMode]),
              default=HighlightingMode.PRECEDING.value, help='Select highlighting mode')
def main(file_name: str, node_name: str, mode: HighlightingMode):
    """Console script for terragraph."""
    if file_name:
        create_highlighted_svg(file_name, node_name, mode=HighlightingMode(mode))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
