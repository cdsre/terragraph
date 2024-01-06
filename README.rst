==========
terragraph
==========


.. image:: https://img.shields.io/pypi/v/terragraph.svg
        :target: https://pypi.python.org/pypi/terragraph

.. image:: https://img.shields.io/travis/cdsre/terragraph.svg
        :target: https://travis-ci.com/cdsre/terragraph

.. image:: https://readthedocs.org/projects/terragraph/badge/?version=latest
        :target: https://terragraph.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




A package to help vizualise output from terraform graph as an svg file


* Free software: MIT license
* Documentation: https://terragraph.readthedocs.io.

Overview
--------

The idea behind this is to choose a node on a terraform dependency graph and be able to highlight all the preceding or
successor edges or both, recursively.

Terraform is pretty good at calculating dependencies however sometimes there are casues where terraform cannot know. or
where users don't realise how terraform generates dependencies. This can lead to race conditions where running the first
time fails but running the second time works. A prime example of this is when we pass an output of module A as an input
of module B. In most cases users assume that outputs of module A will not be available until all resources in the module
have finished. However, this is not the case. Terraform will start running module B as soon as the output in module A is
available even when other resources in module A are not finished but module B expects them to be.

Generating a terraform graph is easy. However, these graphs can get very large very quickly. So trying to follow and
understand the dependencies of one resource in relation to other resources can get complicated. This project attempts to
solve that by taking the output from a `terraform graph` command and selecting a specific node to highlight dependenices.
it provides a HighlightingMode to allow the user to decide if they want to see all the resources the node depends on, all
the resources that depend on this node, or both.

Usage
-----

Currently, this is pretty raw, it just runs at the command line taking the DOT format file and the node name to highlight.
By default it will highlight all **PRECEDING** edges. These are the things that must be completed before this node can
start. It also supports passing the mode as a flag. The modes are

.. table:: mode flags

    ========= ===========
    Value     Description
    ========= ===========
    PRECEDING Highlights all preceding edges to this node. This is all things that needs to complete before this node start
    SUCCESSOR Highlights all successor edges from this node. This is all things that cannot start until this node is completed
    ALL       This applies both PRECEDING and SUCCESSOR modes to highlight the full up and down dependency tree for the node
    ========= ===========


.. code-block:: sh

    terragraph --file-name docs/assets/graph.dot --node-name '"[root] module.mod2.random_pet.this (expand)"'
    Colored node SVG file generated: docs/assets/graph.dot.svg



The above will create an SVG file with the preceding edges highlighted.

.. image:: /docs/assets/graph.dot.svg
   :alt: graph_output


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
