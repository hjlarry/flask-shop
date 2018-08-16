from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField

from .models import ShippingMethod


class ShippingMethodForm(FlaskForm):
    shipping_method = SelectField('Shipping Method', )
    note = TextAreaField('ADD A NOTE TO YOUR ORDER')

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super().__init__(*args, **kwargs)
        self.shipping_method.choices = [(str(vari.id), vari) for vari in ShippingMethod.query.all()]
