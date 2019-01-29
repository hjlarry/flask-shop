from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from .models import DashboardMenu


class DashboardMenuForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    order = IntegerField(default=0)
    endpoint = StringField()
    icon_cls = StringField()
    submit = SubmitField()
