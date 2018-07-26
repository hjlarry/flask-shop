from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class AddCartForm(FlaskForm):
    """add cart form."""

    variant = RadioField(
        "variant",
    )
    quantity = StringField(
        "quantity", validators=[DataRequired()], default=1
    )

    def __init__(self, *args, product=None, **kwargs):
        """Create instance."""
        super().__init__(*args, **kwargs)
        if product:
            self.variant.choices = [(vari.id, vari) for vari in product.variant]


class FilterForm(FlaskForm):
    price = StringField(
        "quantity",
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super().__init__(*args, **kwargs)
