"""
Colorizing functions and structures.
"""

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

    def _get_color_pair(self, color_tag, context_color_tag=None):
        if isinstance(color_tag, basestring):
            pair = self.color_map.get(color_tag)

            if pair:
                pairs = [pair]
            else:
                pairs = []
        else:
            pairs = (
                self.color_map.get(tag)
                for tag in color_tag
            )
            pairs = [pair for pair in pairs if pair is not None]

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
            color_pair = self._get_color_pair(color_tag, context_color_tag)

            if color_pair:
                start, stop = color_pair

                return '{start}{obj}{stop}'.format(
                    start=start,
                    obj=obj,
                    stop=stop,
                )

        return obj


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
