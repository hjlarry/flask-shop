from flask_wtf import FlaskForm as _FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SubmitField,
    SelectField,
    RadioField,
    TextAreaField,
    BooleanField,
    PasswordField,
)
from wtforms.validators import DataRequired


class FlaskForm(_FlaskForm):
    def validate(self, extra_validators=None):
        self._errors = None
        success = True
        for name, field in self._fields.items():
            if field.type in ("SelectField", "SelectMultipleField", "RadioField"):
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


class SiteMenuForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    order = IntegerField(default=0)
    url_ = StringField("Url")
    parent_id = SelectField("Parent")
    site_id = RadioField("Position", choices=[(1, "top"), (2, "bottom")])
    category_id = SelectField("Category")
    collection_id = SelectField("Collection")
    page_id = SelectField("Page")
    submit = SubmitField()


class SitePageForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    slug = StringField()
    content = TextAreaField()
    is_visible = BooleanField()
    submit = SubmitField()


class UserForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    password = PasswordField()
    is_active = BooleanField()
    is_admin = BooleanField()
    submit = SubmitField()
