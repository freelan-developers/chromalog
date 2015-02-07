"""
Mark log entries as important.
"""


class Important(object):
    """
    Wraps any object an mark it as important for logging output.
    """
    def __init__(self, obj):
        """
        Mark `obj` as important.

        :param obj: The object to mark as being important.
        """
        self.obj = obj

    def __str__(self):
        return str(self.obj)

    def __unicode__(self):
        return unicode(self.obj)

    def __eq__(self, other):
        return self.obj == other.obj


def hl(obj):
    """
    Mark an object as important for logging output.

    :param obj: The object to mark as being important.
    :return: A wrapped version of `obj` marked as being important.
    """
    return Important(obj)
