
Lefthook
========

Wrapper for `lefthook <https://github.com/Arkweid/lefthook>`_ to make it installable in the Python ecosystem. Add it into your project dependencies if you want to use lefthook in your Python project.

Installation
------------

.. code-block:: bash

   python3 -m pip install --user lefthook

Usage
-----

You can use this module as proxy for original lefthook. It can be installed on the first execution.

.. code-block:: bash

   python3 -m lefthook --help

This command will install the latest lefthook release and call ``lefthook --help``. Now, you can use lefthook directly:

.. code-block:: bash

   lefthook --help
