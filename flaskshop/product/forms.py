from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class AddCartForm(FlaskForm):
    """add cart form."""

    variant = StringField(
        "variant", validators=[DataRequired()]
    )
    quantity = StringField(
        "quantity", validators=[DataRequired()], default=1
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super().__init__(*args, **kwargs)
