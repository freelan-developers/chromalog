"""
Mark log entries as important.
"""
from builtins import str
from six import string_types

from .colorizer import ColorizableMixin


class Mark(ColorizableMixin):
    """
    Wraps any object an mark it for colored output.
    """
    def __init__(self, obj, color_tag):
        """
        Mark `obj`.

        :param obj: The object to mark for colored output.
        :param color_tag: The color tag to use for coloring.
        """
        if isinstance(obj, Mark):
            if isinstance(color_tag, string_types):
                color_tag = [color_tag]

            if isinstance(obj.color_tag, string_types):
                color_tag.append(obj.color_tag)
            else:
                color_tag.extend(obj.color_tag)

            obj = obj.obj

        super(Mark, self).__init__(color_tag=color_tag)
        self.obj = obj

    def __str__(self):
        return str(self.obj)


def success(obj):
    """
    A convenience helper method that marks an object with the `'success'` color
    tag.

    :param obj: The object the mark.
    :returns: A :class:`Mark<chromalog.mark.Mark>` instance.

    >>> success(42).color_tag
    'success'
    """
    return Mark(obj, color_tag='success')


def error(obj):
    """
    A convenience helper method that marks an object with the `'error'` color
    tag.

    :param obj: The object the mark.
    :returns: A :class:`Mark<chromalog.mark.Mark>` instance.

    >>> error(42).color_tag
    'error'
    """
    return Mark(obj, color_tag='error')


def important(obj):
    """
    A convenience helper method that marks an object with the `'important'`
    color tag.

    :param obj: The object the mark.
    :returns: A :class:`Mark<chromalog.mark.Mark>` instance.

    >>> important(42).color_tag
    'important'
    """
    return Mark(obj, color_tag='important')


def success_if(obj, condition=None):
    """
    A convenience helper method that marks an object with the `'success'` color
    tag if `condition` is truthy, and with the `'error'` color tag otherwise.

    :param obj: The object the mark.
    :param condition: The condition to verify. If `condition` is :const:`None`,
        then `obj` is evaluated instead.
    :returns: A :class:`Mark<chromalog.mark.Mark>` instance.

    >>> success_if(42, True).color_tag
    'success'

    >>> success_if(42, False).color_tag
    'error'

    >>> success_if(42).color_tag
    'success'

    >>> success_if(0).color_tag
    'error'
    """
    if condition is None:
        condition = obj

    return Mark(obj, color_tag='success' if condition else 'error')
