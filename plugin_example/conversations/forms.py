from flask_babel import lazy_gettext
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, ValidationError
from wtforms.validators import DataRequired

from flaskshop.account.models import User

from .models import Conversation, Message


class ConversationForm(FlaskForm):
    to_user = StringField(
        lazy_gettext("Recipient"),
        validators=[
            DataRequired(message=lazy_gettext("A valid username is required."))
        ],
    )

    subject = StringField(
        lazy_gettext("Subject"),
        validators=[DataRequired(message=lazy_gettext("A Subject is required."))],
    )

    message = TextAreaField(
        lazy_gettext("Message"),
        validators=[DataRequired(message=lazy_gettext("A message is required."))],
    )

    def validate_to_user(self, field):
        user = User.query.filter_by(username=field.data).first()
        if not user:
            raise ValidationError(
                lazy_gettext("The username you entered does not exist.")
            )
        if user.id == current_user.id:
            raise ValidationError(lazy_gettext("You cannot send a PM to yourself."))

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
        conversation.save()
        message = Message(
            message=self.message.data,
            user_id=from_user,
            conversation_id=conversation.id,
        )
        message.save()


class MessageForm(FlaskForm):
    message = TextAreaField(
        lazy_gettext("Message"),
        validators=[DataRequired(message=lazy_gettext("A message is required."))],
    )

    def save(self, conversation, user_id, unread=False):
        """Saves the form data to the model.

        :param conversation: The Conversation object.
        :param user_id: The id from the user who sent the message.
        :param reciever: If the message should also be stored in the recievers
                         inbox.
        """
        message = Message(
            message=self.message.data, user_id=user_id, conversation_id=conversation.id
        )

        if unread:
            conversation.unread = True
            conversation.save()
        message.save()
