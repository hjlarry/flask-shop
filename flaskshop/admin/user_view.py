from wtforms.fields import PasswordField
from wtforms.validators import Email, DataRequired

from flaskshop.account.models import User
from flaskshop.extensions import db
from .utils import CustomView


class UserView(CustomView):
    column_list = ("id", "username", "email", "active", "is_admin")
    form_excluded_columns = (
        "orders",
        "favor_products",
        "addresses",
        "cart_items",
        "password",
    )
    form_args = dict(email=dict(validators=[Email(), DataRequired()]))
    form_extra_fields = {"this_password": PasswordField("Password")}

    def __init__(self):
        super().__init__(
            User,
            db.session,
            endpoint="user_admin",
            menu_icon_value="fa-user nav-icon",
        )

    def on_model_change(self, form, User, is_created):
        if form.this_password.data:
            User.set_password(form.this_password.data)
