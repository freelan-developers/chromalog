"""
Colorizing functions and structures.
"""
from builtins import object
from six import (
    string_types,
    PY3,
)

from colorama import (
    Fore,
    Back,
    Style,
)

# Hack to define unicode in Python 3 and reach 100% coverage.
unicode = str if PY3 else unicode


class ColorizableMixin(object):
    """
    Make an object colorizable by a colorizer.
    """

    def __init__(self, color_tag=None):
        """
        Initialize a colorizable instance.

        :param color_tag: The color tag to associate to this instance.

        `color_tag` can be either a string or a list of strings.
        """
        super(ColorizableMixin, self).__init__()
        self.color_tag = color_tag


class ColorizedObject(object):
    """
    Wraps any object to colorize it.
    """

    def __init__(self, obj, color_pair=None):
        """
        Initialize the colorized object.

        :param obj: The object to colorize.
        :param color_pair: The (start, stop) pair of color sequences to wrap
            that object in during string rendering.
        """
        self.obj = obj
        self.color_pair = color_pair

    def __repr__(self):
        """
        Gives a representation of the colorized object.
        """
        if not self.color_pair:
            return repr(self.obj)
        else:
            return "{color_start}{obj!r}{color_stop}".format(
                color_start=self.color_pair[0],
                obj=self.obj,
                color_stop=self.color_pair[1],
            )

    def __str__(self):
        """
        Gives a string representation of the colorized object.
        """
        if not self.color_pair:
            return str(self.obj)
        else:
            return "{color_start}{obj}{color_stop}".format(
                color_start=self.color_pair[0],
                obj=self.obj,
                color_stop=self.color_pair[1],
            )

    def __unicode__(self):
        """
        Gives a string representation of the colorized object.
        """
        if not self.color_pair:
            return unicode(self.obj)
        else:
            return u"{color_start}{obj}{color_stop}".format(
                color_start=self.color_pair[0],
                obj=self.obj,
                color_stop=self.color_pair[1],
            )

    def __int__(self):
        """
        Gives an integer representation of the colorized object.
        """
        return int(self.obj)

    def __float__(self):
        """
        Gives a float representation of the colorized object.
        """
        return float(self.obj)

    def __bool__(self):
        """
        Gives a boolean representation of the colorized object.
        """
        return bool(self.obj)

    def __eq__(self, other):
        """
        Compares this colorized object with another.

        :param other: The other instance to compare with.
        :returns: True if `other` is a
        :class:`chromalog.colorizer.ColorizedObject` instance with equal `obj`
            and `color_pair` members.

        >>> ColorizedObject(42) == ColorizedObject(42)
        True

        >>> ColorizedObject(42) == ColorizedObject(24)
        False

        >>> ColorizedObject(42) == ColorizedObject(42, color_pair=('', ''))
        False

        >>> ColorizedObject(42, color_pair=('', '')) == \
            ColorizedObject(42, color_pair=('', ''))
        True

        >>> ColorizedObject(42, color_pair=('a', 'a')) == \
            ColorizedObject(42, color_pair=('b', 'b'))
        False
        """
        if isinstance(other, self.__class__):
            return (
                other.obj == self.obj and
                other.color_pair == self.color_pair
            )


class GenericColorizer(object):
    """
    A class reponsible for colorizing log entries and
    :class:`chromalog.important.Important` objects.
    """
    def __init__(self, color_map=None, default_color_tag=None):
        """
        Initialize a new colorizer with a specified `color_map`.

        :param color_map: A dictionary where the keys are color tags and the
            value are couples of color sequences (start, stop).
        :param default_color_tag: The color tag to default to in case an
            unknown color tag is encountered. If set to a falsy value no
            default is used.
        """
        self.color_map = color_map or self.default_color_map
        self.default_color_tag = default_color_tag

    def get_color_pair(
        self,
        color_tag,
        context_color_tag=None,
        use_default=True,
    ):
        """
        Get the color pairs for the specified `color_tag` and
        `context_color_tag`.

        :param color_tag: A list of color tags.
        :param context_color_tag: A list of color tags to use as a context.
        :param use_default: If :const:`False` then the default value won't be
            used in case the ``color_tag`` is not found in the associated color
            map.
        :returns: A pair of color sequences.
        """
        if isinstance(color_tag, string_types):
            color_tag = [color_tag]

        pairs = list(
            filter(None, (self.color_map.get(tag) for tag in color_tag))
        )

        if not pairs and use_default:
            pair = self.color_map.get(self.default_color_tag)

            if pair:
                pairs = [pair]

        if context_color_tag:
            ctx_pair = self.get_color_pair(
                color_tag=context_color_tag,
                use_default=False,
            )

            if ctx_pair:
                pairs = [ctx_pair[::-1], ctx_pair] + pairs

        return (
            ''.join(x[0] for x in pairs),
            ''.join(x[1] for x in reversed(pairs)),
        )

    def colorize(self, obj, color_tag=None, context_color_tag=None):
        """
        Colorize an object.

        :param obj: The object to colorize.
        :param color_tag: The color tag to use as a default if ``obj`` is not
            marked.
        :param context_color_tag: The color tag to use as context.
        :returns: ``obj`` if ``obj`` is not a colorizable object. A colorized
            string otherwise.

        .. note: A colorizable object must have a truthy-``color_tag``
            attribute.
        """
        color_tag = getattr(obj, 'color_tag', color_tag)

        if color_tag:
            color_pair = self.get_color_pair(
                color_tag=color_tag,
                context_color_tag=context_color_tag,
            )
        else:
            color_pair = None

        return ColorizedObject(obj=obj, color_pair=color_pair)

    def colorize_message(self, message, *args, **kwargs):
        """
        Colorize a message.

        :param message: The message to colorize. If message is a marked object,
            its color tag will be used as a ``context_color_tag``. ``message``
            may contain formatting placeholders as described in
            :func:`str.format`.
        :returns: The colorized message.

        .. warning::
            This function has no way of check the color-capability of any
            stream that the resulting string might be printed to.
        """
        context_color_tag = getattr(message, 'color_tag', None)
        args = [
            self.colorize(arg, context_color_tag=context_color_tag)
            for arg in args
        ]
        kwargs = {
            key: self.colorize(value, context_color_tag=context_color_tag)
            for key, value in kwargs.items()
        }
        if context_color_tag:
            return str(self.colorize(
                str(message).format(*args, **kwargs),
                color_tag=context_color_tag,
            ))
        else:
            return message.format(*args, **kwargs)


class Colorizer(GenericColorizer):
    """
    Colorize log entries.
    """
    default_color_map = {
        'debug': (Style.DIM + Fore.CYAN, Style.RESET_ALL),
        'info': (Style.RESET_ALL, Style.RESET_ALL),
        'important': (Style.BRIGHT, Style.RESET_ALL),
        'success': (Fore.GREEN, Style.RESET_ALL),
        'warning': (Fore.YELLOW, Style.RESET_ALL),
        'error': (Fore.RED, Style.RESET_ALL),
        'critical': (Back.RED, Style.RESET_ALL),
    }


class MonochromaticColorizer(Colorizer):
    """
    Monochromatic colorizer for non-color-capable streams that only highlights
    :class:`chromalog.mark.Mark` objects with an ``important`` color tag.
    """
    default_color_map = {
        'important': ('**', '**'),
    }
