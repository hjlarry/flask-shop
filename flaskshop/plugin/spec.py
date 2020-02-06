from pluggy import HookspecMarker

spec = HookspecMarker("flaskshop")


@spec
def flaskshop_load_blueprints(app):
    """Hook for registering blueprints.

    :param app: The application object.
    """
