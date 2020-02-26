import uuid
from functools import wraps

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    current_app,
)
from flask.views import MethodView
from flask_login import login_required, current_user

from flaskshop.account.models import User
from flaskshop.extensions import db
from .forms import ConversationForm, MessageForm
from .models import Conversation
from .utils import get_message_count

conversations_bp = Blueprint("conversations_bp", __name__, template_folder="templates")


def check_message_box_space(redirect_to=None):
    """Checks the message quota has been exceeded. If thats the case
    it flashes a message and redirects back to some endpoint.

    :param redirect_to: The endpoint to redirect to. If set to ``None`` it
                        will redirect to the ``conversations_bp.inbox``.
    """
    if get_message_count(current_user) >= current_app.config["MESSAGE_QUOTA"]:
        flash(
            "You cannot send any messages anymore because you have reached your message limit.",
            "danger",
        )
        return redirect(redirect_to or url_for("conversations_bp.inbox"))


def require_message_box_space(f):
    """Decorator for :func:`check_message_box_space`."""
    # not sure how this can be done without explicitly providing a decorator
    # for this
    @wraps(f)
    def wrapper(*a, **k):
        return check_message_box_space() or f(*a, **k)

    return wrapper


class Inbox(MethodView):
    decorators = [login_required]

    def get(self):
        page = request.args.get("page", 1, type=int)
        # the inbox will display both, the recieved and the sent messages
        conversations = (
            Conversation.query.filter(
                Conversation.user_id == current_user.id,
                Conversation.draft == False,
                Conversation.trash == False,
            )
            .order_by(Conversation.updated_at.desc())
            .paginate(page, 10, False)
        )

        return render_template("inbox.html", conversations=conversations)


class ViewConversation(MethodView):
    decorators = [login_required]
    form = MessageForm

    def get(self, conversation_id):
        conversation = Conversation.query.filter_by(
            id=conversation_id, user_id=current_user.id
        ).first_or_404()

        if conversation.unread:
            conversation.unread = False
            conversation.save()

        form = self.form()
        return render_template(
            "conversation.html", conversation=conversation, form=form
        )

    @require_message_box_space
    def post(self, conversation_id):
        conversation = Conversation.query.filter_by(
            id=conversation_id, user_id=current_user.id
        ).first_or_404()

        form = self.form()
        if form.validate_on_submit():
            to_user_id = None
            # If the current_user is the user who recieved the message
            # then we have to change the id's a bit.
            if current_user.id == conversation.to_user_id:
                to_user_id = conversation.from_user_id
            else:
                to_user_id = conversation.to_user_id

            form.save(conversation=conversation, user_id=current_user.id)

            # save the message in the recievers conversation
            old_conv = conversation
            conversation = Conversation.query.filter(
                Conversation.user_id == to_user_id,
                Conversation.shared_id == conversation.shared_id,
            ).first()

            # user deleted the conversation, start a new conversation with just
            # the recieving message
            if conversation is None:
                conversation = Conversation(
                    subject=old_conv.subject,
                    from_user_id=current_user.id,
                    to_user_id=to_user_id,
                    user_id=to_user_id,
                    shared_id=old_conv.shared_id,
                )
                conversation.save()

            form.save(conversation=conversation, user_id=current_user.id, unread=True)

            return redirect(
                url_for(
                    "conversations_bp.view_conversation", conversation_id=old_conv.id
                )
            )

        return render_template(
            "conversation.html", conversation=conversation, form=form
        )


class NewConversation(MethodView):
    decorators = [login_required]
    form = ConversationForm

    def get(self):
        form = self.form()
        form.to_user.data = request.args.get("to_user")
        return render_template("message_form.html", form=form, title="Compose Message")

    def post(self):
        form = self.form()
        if form.validate():
            check_message_box_space()

            to_user = User.query.filter_by(username=form.to_user.data).first()

            # this is the shared id between conversations because the messages
            # are saved on both ends
            shared_id = uuid.uuid4().hex

            # Save the message in the current users inbox
            form.save(
                from_user=current_user.id,
                to_user=to_user.id,
                user_id=current_user.id,
                unread=False,
                shared_id=shared_id,
            )

            # Save the message in the recievers inbox
            form.save(
                from_user=current_user.id,
                to_user=to_user.id,
                user_id=to_user.id,
                unread=True,
                shared_id=shared_id,
            )
            # invalidate_cache(to_user)

            flash("Message sent.", "success")
            return redirect(url_for("conversations_bp.sent"))

        return render_template("message_form.html", form=form)


class MoveConversation(MethodView):
    decorators = [login_required]

    def post(self, conversation_id):
        conversation = Conversation.query.filter_by(
            id=conversation_id, user_id=current_user.id
        ).first_or_404()

        conversation.trash = True
        conversation.save()

        return redirect(url_for("conversations_bp.inbox"))


class RestoreConversation(MethodView):
    decorators = [login_required]

    def post(self, conversation_id):
        conversation = Conversation.query.filter_by(
            id=conversation_id, user_id=current_user.id
        ).first_or_404()

        conversation.trash = False
        conversation.save()
        return redirect(url_for("conversations_bp.trash"))


class DeleteConversation(MethodView):
    decorators = [login_required]

    def post(self, conversation_id):
        conversation = Conversation.query.filter_by(
            id=conversation_id, user_id=current_user.id
        ).first_or_404()

        conversation.delete()
        return redirect(url_for("conversations_bp.trash"))


class SentMessages(MethodView):
    decorators = [login_required]

    def get(self):

        page = request.args.get("page", 1, type=int)

        conversations = (
            Conversation.query.filter(
                Conversation.user_id == current_user.id,
                Conversation.draft == False,
                Conversation.trash == False,
                db.not_(Conversation.to_user_id == current_user.id),
            )
            .order_by(Conversation.updated_at.desc())
            .paginate(page, 10, False)
        )

        return render_template("sent.html", conversations=conversations)


class TrashedMessages(MethodView):
    decorators = [login_required]

    def get(self):

        page = request.args.get("page", 1, type=int)

        conversations = (
            Conversation.query.filter(
                Conversation.user_id == current_user.id, Conversation.trash == True,
            )
            .order_by(Conversation.updated_at.desc())
            .paginate(page, 10, False)
        )

        return render_template("trash.html", conversations=conversations)


conversations_bp.add_url_rule(
    "/new", view_func=NewConversation.as_view("new_conversation")
)
conversations_bp.add_url_rule("/", view_func=Inbox.as_view("index"))
conversations_bp.add_url_rule("/inbox", view_func=Inbox.as_view("inbox"))
conversations_bp.add_url_rule("/sent", view_func=SentMessages.as_view("sent"))
conversations_bp.add_url_rule("/trash", view_func=TrashedMessages.as_view("trash"))
conversations_bp.add_url_rule(
    "/<int:conversation_id>/view",
    view_func=ViewConversation.as_view("view_conversation"),
)
conversations_bp.add_url_rule(
    "/<int:conversation_id>/move",
    view_func=MoveConversation.as_view("move_conversation"),
)
conversations_bp.add_url_rule(
    "/<int:conversation_id>/restore",
    view_func=RestoreConversation.as_view("restore_conversation"),
)
conversations_bp.add_url_rule(
    "/<int:conversation_id>/delete",
    view_func=DeleteConversation.as_view("delete_conversation"),
)
