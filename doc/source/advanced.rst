.. _advanced:

Advanced usage
==============

We've seen in :ref:`quickstart` how to quickly colorize your logging output.
But **Chromalog** has much more to offer than just that !

.. _marking_functions:

Marking functions
-----------------

The :mod:`chromalog.mark` module contains all **Chromalog**'s marking logic.

Its main component is the :class:`Mark <chromalog.mark.Mark>` class which wraps any Python object and associate it with one or several *color tags*.

Those color tags are evaluated during the formatting phase by the :class:`ColorizingFormatter<chromalog.log.ColorizingFormatter>` and transformed into color sequences, as defined in the :class:`ColorizingStreamHandler<chromalog.log.ColorizingStreamHandler>`'s `color_map`.

To decorate a Python object, one can just do:

.. code-block:: python

   from chromalog.mark import Mark

   marked_value = Mark(value, 'my_color_tag')

You may define several color tags at once, by specifying a list:

.. code-block:: python

   from chromalog.mark import Mark

   marked_value = Mark(value, ['my_color_tag', 'some_other_tag'])

This would actually have the same effect as:

.. code-block:: python

   from chromalog.mark import Mark

   marked_value = Mark(Mark(value, 'some_other_tag'), 'my_color_tag')

Such nested :class:`Mark <chromalog.mark.Mark>` instances are actually flattened automatically and their color tags appended.

.. warning::

   Be careful when specifying several color tags: their order **matters** !

   Depending on the color sequences of your color map, the formatted result might differ.

   See :ref:`color_maps` for an example.

**Chromalog** also comes with several built-in helpers which make marking object even more readable. Those helper take a single argument `obj` that is the object to decorate.

=========================================== ====================== =====================================
Helper                                      Associated `color_tag` Associated effet in default color map
------------------------------------------- ---------------------- -------------------------------------
:func:`success<chromalog.mark.success>`     `success`              green color
:func:`error<chromalog.mark.error>`         `error`                red color
:func:`important<chromalog.mark.important>` `important`            brighter color
=========================================== ====================== =====================================

Note that a :func:`chromalog.mark.success_if` function exists that takes an arbitrary object and an optional condition, which results in a call to either :func:`success<chromalog.mark.success>` or :func:`error<chromalog.mark.error>` depending on the condition.

.. _color_maps:

Color maps
----------

.. toctree::
   :maxdepth: 2
