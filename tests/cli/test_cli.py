"""
Test cases for the CLI
"""
import pytest
from click.testing import CliRunner

from terragraph.cli import terragraph_cli


@pytest.fixture
def runner():
    """
    Creates a CLIRunner
    """
    return CliRunner()


def test_highlight_command(runner, runner_temp_file):
    """
    Will test the highlight command with its default inputs
    """
    # Create a temporary file for testing
    input_file_path = runner_temp_file.absolute()
    output_file_path = f"{input_file_path}.svg"
    result = runner.invoke(
        terragraph_cli,
        [
            "highlight",
            "--file-name",
            input_file_path,
            "--node-name",
            '"[root] module.mod1.random_pet.this2 (expand)"',
        ],
    )

    assert result.exit_code == 0
    assert f"Colored node SVG file generated: {output_file_path}" in result.output


def test_show_nodes_command(runner, runner_temp_file):
    """
    test valid show-nodes command
    """
    input_file_path = runner_temp_file.absolute()
    result = runner.invoke(
        terragraph_cli,
        ["show-nodes", "--file-name", input_file_path],
    )

    expected_nodes = r"""
"[root] module.mod1.random_pet.this (expand)"
"[root] module.mod1.random_pet.this2 (expand)"
"[root] module.mod1.time_sleep.this (expand)"
"[root] module.mod2.random_pet.this (expand)"
"[root] provider[\"registry.terraform.io/hashicorp/random\"]"
"[root] provider[\"registry.terraform.io/hashicorp/time\"]"
"""

    assert result.exit_code == 0
    assert f"file is: {input_file_path}" in result.output
    assert expected_nodes in result.output  # Check if actual nodes are listed


def test_invalid_highlight_mode(runner, runner_temp_file):
    """
    Tests that the command fails for invalid highlight modes
    """
    result = runner.invoke(
        terragraph_cli,
        [
            "highlight",
            "--file-name",
            runner_temp_file.absolute(),
            "--node-name",
            "test-node",
            "--mode",
            "invalid_mode",
        ],
    )

    assert result.exit_code != 0
    assert "Invalid value for '--mode'" in result.output
