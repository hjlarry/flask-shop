from .models import Conversation, Message


def get_message_count(user):
    """Returns the number of private messages of the given user.

    :param user: The user object.
    """
    return Conversation.query.filter(Conversation.user_id == user.id).count()


def get_unread_count(user):
    """Returns the unread message count for the given user.

    :param user: The user object.
    """
    return Conversation.query.filter(
        Conversation.unread, Conversation.user_id == user.id
    ).count()


def get_latest_messages(user):
    """Returns all unread messages for the given user.

    :param user: The user object.
    """
    return (
        Conversation.query.filter(Conversation.unread, Conversation.user_id == user.id)
        .order_by(Conversation.id.desc())
        .limit(99)
        .all()
    )
