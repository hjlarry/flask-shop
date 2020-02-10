from flask import current_app
from jinja2 import Markup


class TemplateEventResult(list):
    """A list subclass for results returned by the hook that
    concatenates the results if converted to string, otherwise it works
    exactly like any other list.
    """

    def __init__(self, items):
        list.__init__(self, items)

    def __str__(self):
        return "".join(map(str, self))


def template_hook(name, silent=True, is_markup=True, **kwargs):
    """Calls the given template hook.

    :param name: The name of the hook.
    :param silent: If set to ``False``, it will raise an exception if a hook
                   doesn't exist. Defauls to ``True``.
    :param is_markup: Determines if the hook should return a Markup object or not.
                      Setting to False returns a TemplateEventResult object. The
                      default is True.
    :param kwargs: Additional kwargs that should be passed to the hook.
    """
    try:
        hook = getattr(current_app.pluggy.hook, name)
        result = TemplateEventResult(hook(**kwargs))
    except AttributeError:  # raised if hook doesn't exist
        if silent:
            return ""
        raise

    if is_markup:
        return Markup(result)

    return result
