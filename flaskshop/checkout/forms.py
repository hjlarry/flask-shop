from flask_wtf import FlaskForm
from wtforms import TextAreaField


class NoteForm(FlaskForm):
    note = TextAreaField("ADD A NOTE TO YOUR ORDER")


class VoucherForm(FlaskForm):
    pass
