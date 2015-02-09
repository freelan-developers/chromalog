"""
Mark log entries as important.
"""

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
            if isinstance(color_tag, basestring):
                color_tag = [color_tag]

            if isinstance(obj.color_tag, basestring):
                color_tag.append(obj.color_tag)
            else:
                color_tag.extend(obj.color_tag)

            obj = obj.obj

        super(Mark, self).__init__(color_tag=color_tag)
        self.obj = obj

    def __str__(self):
        return str(self.obj)

    def __unicode__(self):
        return unicode(self.obj)
