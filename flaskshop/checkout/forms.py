from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField
from flask_babel import lazy_gettext

class NoteForm(FlaskForm):
    note = TextAreaField(lazy_gettext("ADD A NOTE TO YOUR ORDER"))


class VoucherForm(FlaskForm):
    code = StringField(lazy_gettext('Code'))
