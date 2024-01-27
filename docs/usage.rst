==========
Usage
==========

Terragraph CLI
--------

The terragraph CLI allows you to generate an SVG image of the terraform graph output. This can be useful to help
visualise resource dependencies and understand the order of operations for resource creation or deletion.

The below examples are all based off this original output from terraform graph command.

.. image:: assets/original_graph.svg
    :alt: original_graph

.. code-block::

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

Show Nodes
++++++++++

You may want to know a list of the nodes in the terraform graph. This command will return a list of nodes. You can then
use a node name in later commands to filter or highlight the graph

.. code-block:: sh

   terragraph show-nodes --file-name graph.dot

This will produce a list of node names in the TF graph.

.. code-block:: sh

   terragraph show-nodes --file-name graph.dot
   file is: graph.dot
   "[root] module.mod1.random_pet.this (expand)"
   "[root] module.mod1.random_pet.this2 (expand)"
   "[root] module.mod1.time_sleep.this (expand)"
   "[root] module.mod2.random_pet.this (expand)"
   "[root] provider[\"registry.terraform.io/hashicorp/random\"]"
   "[root] provider[\"registry.terraform.io/hashicorp/time\"]"
   "[root] var.pet_length"

In larger workloads this may produce hundreds of node names.

Highlight
+++++++++

Once you know the node you are interested in you can generate highlighted graphs for the node your are interested in.
Currently the command will output the SVG as a file in the same path as the original file name passed to it but with .svg
appended to it.

Preceding
__________

Preceding mode will highlight paths to all nodes that this node depends on. This is the default mode when no mode value
is passed. Both these commands will produce the same graph.

.. code-block:: sh

   terragraph highlight --file-name graph.dot --node-name '"[root] module.mod2.random_pet.this (expand)"' --mode=preceding
   terragraph highlight --file-name graph.dot --node-name '"[root] module.mod2.random_pet.this (expand)"'


.. image:: assets/preceding_highlight_graph.svg
   :alt: preceding_highlight_graph

Successor
_________

The Successor mode will highlight paths to all nodes that depend on this node.

.. code-block:: sh

   terragraph highlight --file-name graph.dot --node-name '"[root] module.mod2.random_pet.this (expand)"' --mode=successor

.. image:: assets/successor_highlight_graph.svg
   :alt: successor_highlight_graph

All
___
The All mode will highlight both preceeding and successor dependency paths for this node.

.. code-block:: sh

   terragraph highlight --file-name graph.dot --node-name '"[root] module.mod2.random_pet.this (expand)"' --mode=all

.. image:: assets/all_highlight_graph.svg
   :alt: all_highlight_graph

Filtered
++++++++
The command will also accept a --filtered flag which will remove nodes and paths which are not highlighted. This can be
useful for workloads that generate a large volume of nodes and paths. It allows to only view resources that are related
to the node in some direct or indirect way. The below images are generated using the above examples but running with the
--filtered flag

Preceding
_________
.. code-block:: sh

    terragraph highlight --file-name graph.dot --node-name '"[root] module.mod2.random_pet.this (expand)"' --mode=preceding --filtered

.. image:: assets/preceding_filtered_graph.svg

Successor
_________
.. code-block:: sh

    terragraph highlight --file-name graph.dot --node-name '"[root] module.mod2.random_pet.this (expand)"' --mode=successor --filtered

.. image:: assets/successor_filtered_graph.svg

All
_________
.. code-block:: sh

    terragraph highlight --file-name graph.dot --node-name '"[root] module.mod2.random_pet.this (expand)"' --mode=all --filtered

.. image:: assets/all_filtered_graph.svg
