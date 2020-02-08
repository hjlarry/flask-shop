from .models import Conversation, Message


def get_message_count(user):
    """Returns the number of private messages of the given user.

    :param user: The user object.
    """
    return Conversation.query.filter(
        Conversation.user_id == user.id
    ).count()