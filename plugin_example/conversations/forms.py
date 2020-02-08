from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, TextAreaField, ValidationError
from wtforms.validators import DataRequired

from flaskshop.account.models import User

from .models import Message, Conversation


class ConversationForm(FlaskForm):
    to_user = StringField(
        "Recipient",
        validators=[DataRequired(message="A valid username is required.")],
    )

    subject = StringField(
        "Subject",
        validators=[DataRequired(message="A Subject is required.")],
    )

    message = TextAreaField(
        "Message",
        validators=[DataRequired(message="A message is required.")],
    )


    def validate_to_user(self, field):
        user = User.query.filter_by(username=field.data).first()
        if not user:
            raise ValidationError(
                "The username you entered does not " "exist."
            )
        if user.id == current_user.id:
            raise ValidationError("You cannot send a PM to yourself.")

    def save(self, from_user, to_user, user_id, unread, as_draft=False, shared_id=None):
        conversation = Conversation(
            subject=self.subject.data,
            draft=as_draft,
            shared_id=shared_id,
            from_user_id=from_user,
            to_user_id=to_user,
            user_id=user_id,
            unread=unread,
        )
        message = Message(message=self.message.data, user_id=from_user)
        return conversation.save(message=message)