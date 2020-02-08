import uuid

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask.views import MethodView
from flask_login import login_required, current_user

from flaskshop.account.models import User
from .forms import ConversationForm

conversations_bp = Blueprint("conversations_bp", __name__, template_folder="templates")


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
            shared_id = uuid.uuid4()
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
            # check_message_box_space()

            to_user = User.query.filter_by(username=form.to_user.data).first()

            # this is the shared id between conversations because the messages
            # are saved on both ends
            shared_id = uuid.uuid4()

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


conversations_bp.add_url_rule('/new', view_func=NewConversation.as_view("new_conversation"))