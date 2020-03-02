import pkg_resources
from flask import current_app
from jinja2 import Markup
from email import message_from_string


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


def parse_pkg_metadata(dist_name):
    try:
        raw_metadata = pkg_resources.get_distribution(dist_name).get_metadata(
            "METADATA"
        )
    except FileNotFoundError:
        raw_metadata = pkg_resources.get_distribution(dist_name).get_metadata(
            "PKG-INFO"
        )

    metadata = {}

    # lets use the Parser from email to parse our metadata :)
    for key, value in message_from_string(raw_metadata).items():
        metadata[key.replace("-", "_").lower()] = value

    return metadata
