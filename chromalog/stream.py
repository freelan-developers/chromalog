"""
Stream utilities.
"""


def stream_has_color_support(stream):
    """
    Check if a stream has color support.

    :param stream: The stream to check.
    :returns: True if stream has color support.
    """
    return getattr(stream, 'isatty', lambda: False)()
