"""
Mark log entries as important.
"""

from .colorizer import ColorizableMixin


class Important(ColorizableMixin):
    """
    Wraps any object an mark it as important for logging output.
    """
    def __init__(self, obj, color_tag='important'):
        """
        Mark `obj` as important.

        :param obj: The object to mark as being important.
        :param color_tag: The color tag to use.
        """
        if isinstance(obj, Important):
            if isinstance(color_tag, basestring):
                color_tag = [color_tag]

            if isinstance(obj.color_tag, basestring):
                color_tag.append(obj.color_tag)
            else:
                color_tag.extend(obj.color_tag)

            obj = obj.obj

        super(Important, self).__init__(color_tag=color_tag)
        self.obj = obj

    def __str__(self):
        return str(self.obj)

    def __unicode__(self):
        return unicode(self.obj)
