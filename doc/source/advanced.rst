.. _advanced:

Advanced usage
==============

We've seen in :ref:`quickstart` how to quickly colorize your logging output.
But **Chromalog** has much more to offer than just that !

.. _marking_functions:

Marking functions
-----------------

The :mod:`chromalog.mark` module contains all **Chromalog**'s marking logic.

Its main component is the :class:`Mark <chromalog.mark.Mark>` class which wraps
any Python object and associate it with one or several *color tags*.

Those color tags are evaluated during the formatting phase by the
:class:`ColorizingFormatter<chromalog.log.ColorizingFormatter>` and transformed
into color sequences, as defined in the
:class:`ColorizingStreamHandler<chromalog.log.ColorizingStreamHandler>`'s
`color_map`.

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

Such nested :class:`Mark <chromalog.mark.Mark>` instances are actually
flattened automatically and their color tags appended.

.. warning::

   Be careful when specifying several color tags: their order **matters** !

   Depending on the color sequences of your color map, the formatted result
   might differ.

   See :ref:`color_maps` for an example.

**Chromalog** also comes with several built-in helpers which make marking
object even more readable. Those helpers are generated automatically by several
*magic* modules.

Simple helpers
##############

Simple helpers are a quick way of marking an object and an efficient way of
conveying meaning.

You can generate simple helpers by importing them from the
:mod:`chromalog.mark.helpers.simple` magic module:

.. doctest::

   >>> from chromalog.mark.helpers.simple import important

   >>> important(42).color_tag
   ['important']

Like :class:`Mark<chromalog.mark.Mark>` instance, you can obviously combine
several helpers to cumulate the effects.

.. doctest::

   >>> from chromalog.mark.helpers.simple import important, success

   >>> important(success(42)).color_tag
   ['important', 'success']

If the name of the helper you want to generate is not a suitable python
identifier, you can use the :func:`chromalog.mark.helpers.simple.make_helper`
function instead.

Note that, should you need it, documentation is generated for each helper. For
instance, here is the generated documentation for the
:func:`chromalog.mark.helpers.simple.success` function:

.. autofunction:: chromalog.mark.helpers.simple.success

Conditional helpers
###################

Conditional helpers are a quick way of using a header depending on a boolean
condition.

You can generate conditional helpers by importing them from the
:mod:`chromalog.mark.helpers.conditional` magic module:

.. doctest::

   >>> from chromalog.mark.helpers.conditional import success_or_error

   >>> success_or_error(42, True).color_tag
   ['success']

   >>> success_or_error(42, False).color_tag
   ['error']

.. note::

   The only requirement for the helper is that it must have a name of the form
   ``a_or_b`` where ``a`` and ``b`` are color tags.

If the name of the helper you want to generate is not a suitable python
identifier, you can use the
:func:`chromalog.mark.helpers.conditional.make_helper` function instead.

Custom marking functions
########################

Defining your custom markers is easy.


.. _color_maps:

Color maps
----------

.. toctree::
   :maxdepth: 2
