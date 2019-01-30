from flask_wtf import FlaskForm as _FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired


class FlaskForm(_FlaskForm):
    def validate(self, extra_validators=None):
        self._errors = None
        success = True
        for name, field in self._fields.items():
            if field.type in ("SelectField", "SelectMultipleField"):
                continue
            if extra_validators is not None and name in extra_validators:
                extra = extra_validators[name]
            else:
                extra = tuple()
            if not field.validate(self, extra):
                success = False
        return success


class DashboardMenuForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    order = IntegerField(default=0)
    endpoint = StringField()
    icon_cls = StringField()
    parent_id = SelectField("Parent")
    submit = SubmitField()
