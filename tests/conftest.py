"""
The general fixutres for pytest
"""
import pytest

from terragraph.core import Terragraph


@pytest.fixture()
def graph_string() -> str:
    """
    Creates an example digraph based on a terraform output
    :return:
    """
    return r"""
digraph {
	compound = "true"
	newrank = "true"
	subgraph "root" {
		"[root] module.mod1.random_pet.this (expand)" [label = "module.mod1.random_pet.this", shape = "box"]
		"[root] module.mod1.random_pet.this2 (expand)" [label = "module.mod1.random_pet.this2", shape = "box"]
		"[root] module.mod1.time_sleep.this (expand)" [label = "module.mod1.time_sleep.this", shape = "box"]
		"[root] module.mod2.random_pet.this (expand)" [label = "module.mod2.random_pet.this", shape = "box"]
		"[root] provider[\"registry.terraform.io/hashicorp/random\"]" [label = "provider[\"registry.terraform.io/hashicorp/random\"]", shape = "diamond"]
		"[root] provider[\"registry.terraform.io/hashicorp/time\"]" [label = "provider[\"registry.terraform.io/hashicorp/time\"]", shape = "diamond"]
		"[root] var.pet_length" [label = "var.pet_length", shape = "note"]
		"[root] module.mod1 (close)" -> "[root] module.mod1.output.pet (expand)"
		"[root] module.mod1 (close)" -> "[root] module.mod1.output.pet_length (expand)"
		"[root] module.mod1 (close)" -> "[root] module.mod1.random_pet.this2 (expand)"
		"[root] module.mod1.output.pet (expand)" -> "[root] module.mod1.random_pet.this (expand)"
		"[root] module.mod1.output.pet_length (expand)" -> "[root] module.mod1.random_pet.this (expand)"
		"[root] module.mod1.random_pet.this (expand)" -> "[root] module.mod1.var.pet_length (expand)"
		"[root] module.mod1.random_pet.this (expand)" -> "[root] provider[\"registry.terraform.io/hashicorp/random\"]"
		"[root] module.mod1.random_pet.this2 (expand)" -> "[root] module.mod1.time_sleep.this (expand)"
		"[root] module.mod1.random_pet.this2 (expand)" -> "[root] module.mod1.var.pet_length (expand)"
		"[root] module.mod1.random_pet.this2 (expand)" -> "[root] provider[\"registry.terraform.io/hashicorp/random\"]"
		"[root] module.mod1.time_sleep.this (expand)" -> "[root] module.mod1 (expand)"
		"[root] module.mod1.time_sleep.this (expand)" -> "[root] provider[\"registry.terraform.io/hashicorp/time\"]"
		"[root] module.mod1.var.pet_length (expand)" -> "[root] module.mod1 (expand)"
		"[root] module.mod1.var.pet_length (expand)" -> "[root] var.pet_length"
		"[root] module.mod2 (close)" -> "[root] module.mod2.random_pet.this (expand)"
		"[root] module.mod2.random_pet.this (expand)" -> "[root] module.mod2.var.pet_length (expand)"
		"[root] module.mod2.var.pet_length (expand)" -> "[root] module.mod1.output.pet (expand)"
		"[root] module.mod2.var.pet_length (expand)" -> "[root] module.mod2 (expand)"
		"[root] provider[\"registry.terraform.io/hashicorp/random\"] (close)" -> "[root] module.mod1.random_pet.this2 (expand)"
		"[root] provider[\"registry.terraform.io/hashicorp/random\"] (close)" -> "[root] module.mod2.random_pet.this (expand)"
		"[root] provider[\"registry.terraform.io/hashicorp/time\"] (close)" -> "[root] module.mod1.time_sleep.this (expand)"
		"[root] root" -> "[root] module.mod1 (close)"
		"[root] root" -> "[root] module.mod2 (close)"
		"[root] root" -> "[root] provider[\"registry.terraform.io/hashicorp/random\"] (close)"
		"[root] root" -> "[root] provider[\"registry.terraform.io/hashicorp/time\"] (close)"
	}
}
"""


@pytest.fixture()
def terragraph_example(graph_string) -> Terragraph:
    """
    creates a Terragraph object form the example graph_string
    :param graph_string:
    :return: Terraggraph object
    """
    return Terragraph(dot_data=graph_string)


@pytest.fixture()
def runner_temp_file(tmp_path, graph_string):
    """
    Creates a temp file for the runner to use with a terraform graph in it
    """
    # Create a temporary file for testing
    test_file = tmp_path / "graph.dot"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(graph_string)
        f.flush()
        yield test_file
