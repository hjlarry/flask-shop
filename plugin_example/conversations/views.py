import uuid

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask.views import MethodView
from flask_login import login_required, current_user

from flaskshop.account.models import User
from .forms import ConversationForm
from .models import Conversation
from .utils import get_message_count

conversations_bp = Blueprint("conversations_bp", __name__, template_folder="templates")


def check_message_box_space(redirect_to=None):
    """Checks the message quota has been exceeded. If thats the case
    it flashes a message and redirects back to some endpoint.

    :param redirect_to: The endpoint to redirect to. If set to ``None`` it
                        will redirect to the ``conversations_bp.inbox``
                        endpoint.
    """
    if get_message_count(current_user) >= current_app.config["MESSAGE_QUOTA"]:
        flash("You cannot send any messages anymore because you have reached your message limit.", "danger")
        return redirect(redirect_to or url_for("conversations_bp.inbox"))


class NewConversation(MethodView):
    decorators = [login_required]
    form = ConversationForm

    def get(self):
        form = self.form()
        form.to_user.data = request.args.get("to_user")
        return render_template(
            "message_form.html", form=form, title="Compose Message"
        )

    def post(self):
        form = self.form()
        if "save_message" in request.form and form.validate():
            to_user = User.query.filter_by(username=form.to_user.data).first()
            shared_id = uuid.uuid4().hex
            form.save(
                from_user=current_user.id,
                to_user=to_user.id,
                user_id=current_user.id,
                unread=False,
                as_draft=True,
                shared_id=shared_id,
            )

            flash("Message saved.", "success")
            return redirect(url_for("conversations_bp.drafts"))

        if "send_message" in request.form and form.validate():
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

        return render_template(
            "message_form.html", form=form, title="Compose Message"
        )


class DraftMessages(MethodView):
    decorators = [login_required]

    def get(self):

        page = request.args.get('page', 1, type=int)

        conversations = Conversation.query. \
            filter(
                Conversation.user_id == current_user.id,
                Conversation.draft == True,
                Conversation.trash == False
            ).\
            order_by(Conversation.updated_at.desc()). \
            paginate(page, 10, False)

        return render_template(
            "drafts.html", conversations=conversations
        )

conversations_bp.add_url_rule('/new', view_func=NewConversation.as_view("new_conversation"))
conversations_bp.add_url_rule('/drafts', view_func=DraftMessages.as_view("drafts"))