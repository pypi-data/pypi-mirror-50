
FlakeHell
=========

It's a `Flake8 <https://gitlab.com/pycqa/flake8>`_ wrapper to make it cool.


* Use only specified plugins, not everything installed.
* Manage codes per plugin.
* Enable and disable plugins and codes by wildcard.
* Make output beautiful.
* Show codes for installed plugins.
* Show all messages and codes for a plugin.
* Check that all required plugins are installed.
* Syntax highlighting in messages and code snippets.


.. image:: ./assets/grouped.png
   :target: ./assets/grouped.png
   :alt: output example


Installation
------------

.. code-block::

   python3 -m pip install --user flakehell

Usage
-----

First of all, let's create ``pyproject.toml`` config:

.. code-block::

   [tool.flakehell]
   exclude = ["example.py"]
   format = "grouped"
   max_line_length = 90
   show_source = true

   [tool.flakehell.plugins]
   pyflakes = ["+*", "-F401"]
   flake8-quotes = ["+*"]


* You can specify any flake8 settings in ``[tool.flakehell]``.
* ``[tool.flakehell.plugins]`` contains list of plugins and rules for them.

Show plugins that aren't installed yet:

.. code-block:: bash

   flakehell missed

Show installed plugins, used plugins, specified rules, codes prefixes:

.. code-block:: bash

   flakehell plugins


.. image:: ./assets/plugins.png
   :target: ./assets/plugins.png
   :alt: plugins command output


Show codes and messages for a specific plugin:

.. code-block:: bash

   flakehell codes pyflakes


.. image:: ./assets/codes.png
   :target: ./assets/codes.png
   :alt: codes command output


Run flake8 against the code:

.. code-block:: bash

   flakehell lint

This command accepts all the same arguments as Flake8.

Formatters
----------

Formatters make errors output nice. Available formatters:


* ``colored`` -- for humans.
* ``grouped`` -- also colored, but all messages are explicitly grouped by file.
* ``json`` -- no colors, only one json-dict per line for every error.

Also, you can specify ``show_source = true`` in the config to show line of source code where error occurred with syntax highlighting.

Colored:


.. image:: ./assets/colored.png
   :target: ./assets/colored.png
   :alt: colored


Colored with source code:


.. image:: ./assets/colored-source.png
   :target: ./assets/colored-source.png
   :alt: colored


Grouped:


.. image:: ./assets/grouped.png
   :target: ./assets/grouped.png
   :alt: grouped


Grouped with source code:


.. image:: ./assets/grouped-source.png
   :target: ./assets/grouped-source.png
   :alt: grouped


JSON:


.. image:: ./assets/json.png
   :target: ./assets/json.png
   :alt: json

