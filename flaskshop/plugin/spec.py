from pluggy import HookspecMarker

spec = HookspecMarker("flaskshop")


@spec
def flaskshop_load_blueprints(app):
    """Hook for registering blueprints.

    :param app: The application object.
    """


@spec
def flaskbb_tpl_user_nav_loggedin_before():
    """Hook for registering additional user navigational items
    which are only shown when a user is logged in.

    in :file:`templates/layout.html`.
    """
