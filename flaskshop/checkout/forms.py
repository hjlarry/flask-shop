from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField
from flask_babel import gettext

class NoteForm(FlaskForm):
    note = TextAreaField(gettext("ADD A NOTE TO YOUR ORDER"))


class VoucherForm(FlaskForm):
    code = StringField()
