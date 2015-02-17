.. _installation:

Installation
============

Using pip
---------

The simplest way to install **Chromalog** is to use `pip
<https://pypi.python.org/pypi/pip/>`_.

Just type the following command in your command prompt:

.. code-block:: bash

   pip install chromalog

That's it ! No configuration is needed. **Chromalog** is
now installed on your system.

From source
-----------

If you feel in hacky mood, you can also install
**Chromalog** from `source
<https://github.com/freelan-developers/chromalog>`_.

Clone the Git repository:

.. code-block:: bash

   git clone git@github.com:freelan-developers/chromalog.git

Then, inside the cloned repository folder:

.. code-block:: bash

   python setup.py install

And that's it ! **Chromalog** should now be installed in
your Python packages.

You can easily test it by typing in a command prompt:

.. code-block:: bash

   python -c "import chromalog"

This should not raise any error (especially not an
:py:exc:`ImportError`).

.. toctree::
   :maxdepth: 3

What's next ?
-------------

:ref:`Get started <quickstart>` or explore :ref:`api`.
