"""
Automatically generate marking helpers functions.
"""

import sys

from .objects import Mark


class HelpersModule(object):
    """
    A class that is designed to replace the module and implement magic helper
    generation.
    """

    Mark = Mark
    __name__ = __name__
    __file__ = __file__

    def __init__(self):
        self.__helpers = {}
        self.__conditional_helpers = {}

    def make_helper(self, color_tag):
        """
        Make a simple helper.

        :param color_tag: The color tag to make a helper for.
        :returns: The helper function.
        """
        helper = self.__helpers.get(color_tag)

        if not helper:
            def helper(obj):
                return self.Mark(obj=obj, color_tag=color_tag)

            helper.__name__ = color_tag
            helper.__doc__ = """
            Mark an object for coloration.

            The color tag is set to {color_tag!r}.

            :param obj: The object to mark for coloration.
            :returns: A :class:`Mark<chromalog.mark.objects.Mark>` instance.

            >>> {color_tag}(42).color_tag
            ['{color_tag}']
            """.format(color_tag=color_tag)

            self.__helpers[color_tag] = helper

        return helper

    def make_conditional_helper(self, ct_true, ct_false):
        """
        Make a conditional helper.

        :param ct_true: The color tag if the condition is met.
        :param ct_false: The color tag if the condition is not met.
        :returns: The helper function.
        """
        helper = self.__conditional_helpers.get((ct_true, ct_false))

        if not helper:
            def helper(obj, condition=None):
                if condition is None:
                    condition = obj

                return self.Mark(
                    obj=obj,
                    color_tag=ct_true if condition else ct_false,
                )

            helper.__name__ = '_or_'.join((ct_true, ct_false))
            helper.__doc__ = """
            Convenience helper method that marks an object with the {ct_true!r}
            color tag if `condition` is truthy, and with the {ct_false!r} color
            tag otherwise.

            :param obj: The object to mark for coloration.
            :param condition: The condition to verify. If `condition` is
                :const:`None`, the `obj` is evaluated instead.
            :returns: A :class:`Mark<chromalog.mark.objects.Mark>` instance.

            >>> {name}(42, True).color_tag
            ['{ct_true}']

            >>> {name}(42, False).color_tag
            ['{ct_false}']

            >>> {name}(42).color_tag
            ['{ct_true}']

            >>> {name}(0).color_tag
            ['{ct_false}']
            """.format(
                name=helper.__name__,
                ct_true=ct_true,
                ct_false=ct_false,
            )

            self.__conditional_helpers[(ct_true, ct_false)] = helper

        return helper

    def __getattr__(self, name):
        """
        Get a magic helper.

        :param name: The name of the helper to get.

        If `name` contains the string '_or_', two color tags are extracted and
        a conditional helper is built.
        """
        if name.startswith('__'):
            raise AttributeError(name)

        # This prevents nosetests from trying to interpret this fake module as
        # a test module.
        if name in {
                'im_class',
                'setup_module',
                'setupModule',
                'setUpModule',
                'setup',
                'setUp',
                'teardown_module',
                'teardownModule',
                'tearDownModule',
                'teardown',
                'tearDown',
        }:
            raise AttributeError(name)

        if '_or_' in name:
            ct_true, ct_false = name.split('_or_')
            return self.make_conditional_helper(
                ct_true=ct_true,
                ct_false=ct_false,
            )
        else:
            return self.make_helper(color_tag=name)


ref, sys.modules[__name__] = sys.modules[__name__], HelpersModule()
