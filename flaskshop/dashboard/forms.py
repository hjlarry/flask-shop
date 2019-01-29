from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from .models import DashboardMenu


class DashboardMenuForm(FlaskForm):
    title = StringField()
    order = IntegerField()
    endpoint = StringField()
    icon_cls = StringField()
    submit = SubmitField()
