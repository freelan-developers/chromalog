"""
Colorizing functions and structures.
"""
from builtins import object

from colorama import (
    Fore,
    Back,
    Style,
)


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

        >>> repr(ColorizedObject('a', ('<', '>')))
        "ColorizedObject('a', ('<', '>'))"
        """
        return '{klass}({obj!r}, {color_pair!r})'.format(
            klass=self.__class__.__name__,
            obj=self.obj,
            color_pair=self.color_pair,
        )

    def __str__(self):
        """
        Gives a string representation of the colorized object.

        >>> str(ColorizedObject('a'))
        'a'

        >>> str(ColorizedObject('a', ('<', '>')))
        '<a>'
        """
        if not self.color_pair:
            return str(self.obj)
        else:
            return "{color_start}{obj}{color_stop}".format(
                color_start=self.color_pair[0],
                obj=self.obj,
                color_stop=self.color_pair[1],
            )

    def __int__(self):
        """
        Gives an integer representation of the colorized object.

        >>> int(ColorizedObject(42))
        42
        """
        return int(self.obj)

    def __float__(self):
        """
        Gives a float representation of the colorized object.

        >>> float(ColorizedObject(3.14))
        3.14
        """
        return float(self.obj)

    def __bool__(self):
        """
        Gives a boolean representation of the colorized object.

        >>> bool(ColorizedObject(True))
        True
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

    def get_color_pair(self, color_tag, context_color_tag=None):
        """
        Get the color pairs for the specified `color_tag` and
        `context_color_tag`.

        :param color: A list of color tags.
        :param context_color_tag: A color tag to use as a context.
        :returns: A pair of color sequences.

        >>> Colorizer({}).get_color_pair(['a'])
        ('', '')

        >>> Colorizer({'a': ('[', ']')}).get_color_pair(['a'])
        ('[', ']')

        >>> Colorizer({'a': ('[', ']'), 'b': ('<', '>')}).\
            get_color_pair(['a', 'b'])
        ('[<', '>]')

        >>> Colorizer({'a': ('[', ']'), 'b': ('<', '>')}, 'b').\
            get_color_pair(['c'])
        ('<', '>')

        >>> Colorizer({'a': ('[', ']'), 'b': ('<', '>')}).\
            get_color_pair(['a'], 'b')
        ('><[', ']><')
        """
        pairs = filter(None, (self.color_map.get(tag) for tag in color_tag))

        if not pairs:
            pair = self.color_map.get(self.default_color_tag)

            if pair:
                pairs = [pair]

        if context_color_tag:
            ctx_pair = self.color_map.get(context_color_tag)

            if ctx_pair:
                pairs = [ctx_pair[::-1], ctx_pair] + pairs

        return (
            ''.join(x[0] for x in pairs),
            ''.join(x[1] for x in reversed(pairs)),
        )

    def colorize(self, obj, context_color_tag=None):
        """
        Colorize an object.

        :param obj: The object to colorize.
        :param context_color_tag: The color tag to use as context.
        :returns: `obj` is `obj` is not a colorizable object. A colorized
            string otherwise.

        .. note: A colorizable object must have a truthy-`color_tag` attribute.
        """
        color_tag = getattr(obj, 'color_tag', None)

        if color_tag:
            color_pair = self.get_color_pair(color_tag, context_color_tag)
        else:
            color_pair = None

        return ColorizedObject(obj=obj, color_pair=color_pair)


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
    :class:`chromalog.important.Important` objects.
    """
    default_color_map = {
        'important': ('**', '**'),
    }
