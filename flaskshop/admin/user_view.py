from wtforms.fields import PasswordField
from wtforms.validators import Email, DataRequired
from flask_admin.contrib.sqla.fields import QuerySelectField
from sqlalchemy import orm

from flaskshop.account.models import User, UserAddress
from flaskshop.extensions import db
from .utils import CustomView


class UserView(CustomView):
    column_list = ("id", "username", "email", "active", "is_admin")
    form_excluded_columns = (
        "orders",
        # "addresses",
        "cart",
        "open_id",
        "session_key",
    )
    form_args = dict(email=dict(validators=[Email(), DataRequired()]))
    form_extra_fields = {"this_password": PasswordField("Password")}

    def __init__(self):
        super().__init__(
            User,
            db.session,
            name="User List",
            category="user",
            endpoint="user_admin",
            menu_icon_value="nav-icon",
        )

    def on_model_change(self, form, User, is_created):
        if form.this_password.data:
            User.set_password(form.this_password.data)


def user_query():
    return User.query.options(orm.load_only("id", "username"))


class UserAddressView(CustomView):
    def __init__(self):
        super().__init__(
            UserAddress,
            db.session,
            category="user",
            endpoint="user_address_admin",
            menu_icon_value="nav-icon",
        )

    form_extra_fields = {
        "user_id": QuerySelectField(
            label="User", query_factory=user_query, get_label="username"
        )
    }

