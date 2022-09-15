from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField


class NoteForm(FlaskForm):
    note = TextAreaField(lazy_gettext("ADD A NOTE TO YOUR ORDER"))


class VoucherForm(FlaskForm):
    code = StringField(lazy_gettext("Code"))
