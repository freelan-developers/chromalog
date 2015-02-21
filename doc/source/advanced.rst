.. _advanced:

Advanced usage
==============

.. testsetup::

   from __future__ import print_function

We've seen in :ref:`quickstart` how to quickly colorize your logging output.
But **Chromalog** has much more to offer than just that !

.. _marking_functions:

Marking functions
-----------------

The :mod:`chromalog.mark` module contains all **Chromalog**'s marking logic.

Its main component is the :class:`Mark <chromalog.mark.Mark>` class which wraps
any Python object and associates it with one or several *color tags*.

Those color tags are evaluated during the formatting phase by the
:class:`ColorizingFormatter<chromalog.log.ColorizingFormatter>` and transformed
into color sequences, as defined in the
:class:`ColorizingStreamHandler<chromalog.log.ColorizingStreamHandler>`'s
:ref:`color map<color_maps>`.

To decorate a Python object, one can just do:

.. testcode::

   from chromalog.mark import Mark

   marked_value = Mark('value', 'my_color_tag')

You may define several color tags at once, by specifying a list:

.. testcode::

   from chromalog.mark import Mark

   marked_value = Mark('value', ['my_color_tag', 'some_other_tag'])

Nested :class:`Mark <chromalog.mark.Mark>` instances are actually flattened
automatically and their color tags appended.

.. testcode::

   from chromalog.mark import Mark

   marked_value = Mark(Mark('value', 'some_other_tag'), 'my_color_tag')

.. warning::

   Be careful when specifying several color tags: their order **matters** !

   Depending on the color sequences of your color map, the formatted result
   might differ.

   See :ref:`color_maps` for an example.

Helpers
+++++++

**Chromalog** also comes with several built-in helpers which make marking
objects even more readable. Those helpers are generated automatically by several
*magic* modules.

Simple helpers
##############

Simple helpers are a quick way of marking an object and an explicit way of
highlighting a value.

You can generate simple helpers by importing them from the
:mod:`chromalog.mark.helpers.simple` magic module, like so:

.. testcode::

   from chromalog.mark.helpers.simple import important

   print(important(42).color_tag)

Which gives the following output:

.. testoutput::

   ['important']

An helper function with a color tag similar to its name will be generated and
made accessible transparently.

Like :class:`Mark<chromalog.mark.Mark>` instances, you can obviously combine
several helpers to cumulate the effects.

For instance:

.. testcode::

   from chromalog.mark.helpers.simple import important, success

   print(important(success(42)).color_tag)

Gives:

.. testoutput::

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

Conditional helpers are a quick way of associating a color tag to an object
depending on a boolean condition.

You can generate conditional helpers by importing them from the
:mod:`chromalog.mark.helpers.conditional` magic module:

.. testcode::

   from chromalog.mark.helpers.conditional import success_or_error

   print(success_or_error(42, True).color_tag)
   print(success_or_error(42, False).color_tag)
   print(success_or_error(42).color_tag)
   print(success_or_error(0).color_tag)

Which gives:

.. testoutput::

   ['success']
   ['error']
   ['success']
   ['error']

.. warning::

   Automatically generated conditional helpers must have a name of the form
   ``a_or_b`` where ``a`` and ``b`` are color tags.

If the name of the helper you want to generate is not a suitable python
identifier, you can use the
:func:`chromalog.mark.helpers.conditional.make_helper` function instead.

.. note::

   If no ``condition`` is specified, then the value itself is evaluated as a
   boolean value.

   This is useful for outputing exit codes for instance.

Colorizers
----------

The :class:`GenericColorizer<chromalog.colorizer.GenericColorizer>` class is
responsible for turning color tags into colors (or decoration sequences).

.. _color_maps:

Color maps
++++++++++

To do so, each :class:`GenericColorizer<chromalog.colorizer.GenericColorizer>`
instance has a ``color_map`` :class:`dictionary<dict>` which has the following
structure:

.. code-block:: python

   color_map = {
      'alpha': ('[', ']'),
      'beta': ('{', '}'),
   }

That is, each *key* is the color tag, and each *value* is a pair
``(start_sequence, stop_sequence)`` of start and stop sequences that will
surround the decorated value when it is output.

Values are decorated in order with the seqauences that match their associated
color tags. For instance:

.. testcode::

   from chromalog.mark.helpers.simple import alpha, beta
   from chromalog.colorizer import GenericColorizer

   colorizer = GenericColorizer(color_map={
      'alpha': ('[', ']'),
      'beta': ('{', '}'),
   })

   print(colorizer.colorize(alpha(beta(42))))
   print(colorizer.colorize(beta(alpha(42))))

Which gives:

.. testoutput::

   [{42}]
   {[42]}

Context colorizing
++++++++++++++++++

Note that the :func:`colorize<chromalog.colorizer.GenericColorizer.colorize>`
method takes an optional parameter ``context_color_tag`` which is mainly used
by the :class:`ColorizingFormatter<chromalog.log.ColorizingFormatter>`
to colorize subparts of a colorized message.

``context_color_tag`` should match the color tag used to colorize the
contextual message as a whole. Unless you write your own formatter, you
shouldn't have to care much about it.

Here is an example on how ``context_color_tag`` modifies the output:

.. testcode::

   from chromalog.mark.helpers.simple import alpha
   from chromalog.colorizer import GenericColorizer

   colorizer = GenericColorizer(color_map={
      'alpha': ('[', ']'),
      'beta': ('{', '}'),
   })

   print(colorizer.colorize(alpha(42), context_color_tag='beta'))

Which gives:

.. testoutput::

   }{[42]}{

As you can see, the context color tag is first closed then reopened, then the
usual color tags are used. This behavior is required as it prevents some color
escaping sequences to persist after the tags get closed on some terminals.

Built-in colorizers
+++++++++++++++++++

**Chromalog** ships with two default colorizers:

- :class:`Colorizer<chromalog.colorizer.Colorizer>` which is associated to a
  color map constitued of color escaping sequences.
- :class:`MonochromaticColorizer<chromalog.colorizer.MonochromaticColorizer>`
  which may be used on non color-capable output streams and that only decorates
  objects marked with the ``'important'`` color tag.

See :ref:`default_color_maps` for a comprehensive list of default color tags
and their resulting sequences.

Custom colorizers
#################

One can create its own colorizer by simply deriving from the
:class:`GenericColorizer<chromalog.colorizer.GenericColorizer>` class and
defining the ``default_color_map`` class attribute, like so:

.. testcode::

   from chromalog.colorizer import GenericColorizer

   from colorama import (
      Fore,
      Back,
      Style,
   )

   class MyColorizer(GenericColorizer):
      default_color_map = {
         'success': (Fore.GREEN, Style.RESET_ALL),
      }

Decorating messages
###################

Colorizers also provide a method to directly colorize a message, regardless of any output stream and its color capabilities:

.. automethod:: chromalog.colorizer.GenericColorizer.colorize_message
   :noindex:

Here is an example of usage:

.. testcode::

   from chromalog.colorizer import GenericColorizer
   from chromalog.mark.helpers.simple import alpha

   colorizer = GenericColorizer(color_map={
       'alpha': ('[', ']'),
   })

   print(colorizer.colorize_message(
       'hello {} ! How {are} you ?',
       alpha('world'),
       are=alpha('are'),
   ))

This gives the following output:

.. testoutput::

   hello [world] ! How [are] you ?

.. _default_color_maps:

Default color maps and sequences
################################

Here is a list of the default color tags and their associated sequences:

+-----------------------------------------------------------------------------+-------------+-----------------------------+
| Colorizer                                                                   | Color tag   | Effect                      |
+-----------------------------------------------------------------------------+-------------+-----------------------------+
| :class:`Colorizer<chromalog.colorizer.Colorizer>`                           | `debug`     | Light blue color.           |
|                                                                             +-------------+-----------------------------+
|                                                                             | `info`      | Default terminal style.     |
|                                                                             +-------------+-----------------------------+
|                                                                             | `important` | Brighter output.            |
|                                                                             +-------------+-----------------------------+
|                                                                             | `success`   | Green color.                |
|                                                                             +-------------+-----------------------------+
|                                                                             | `warning`   | Yellow color.               |
|                                                                             +-------------+-----------------------------+
|                                                                             | `error`     | Red color.                  |
|                                                                             +-------------+-----------------------------+
|                                                                             | `critical`  | Red background.             |
+-----------------------------------------------------------------------------+-------------+-----------------------------+
| :class:`MonochromaticColorizer<chromalog.colorizer.MonochromaticColorizer>` | `important` | Value surrounded by ``**``. |
+-----------------------------------------------------------------------------+-------------+-----------------------------+

.. toctree::
   :maxdepth: 3
