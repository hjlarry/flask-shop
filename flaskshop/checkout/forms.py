from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField


class NoteForm(FlaskForm):
    note = TextAreaField("ADD A NOTE TO YOUR ORDER")


class VoucherForm(FlaskForm):
    code = StringField()
