from flaskshop.database import Column, Model, db
from flaskshop.account.models import User


class Message(Model):
    __tablename__ = "conversation_messages"

    conversation_id = Column(db.Integer(), nullable=False)
    user_id = Column(db.Integer(), nullable=False)
    message = Column(db.Text, nullable=False)

    @property
    def user(self):
        return User.query.filter_by(id=self.user_id).first()


class Conversation(Model):
    __tablename__ = "conversation_dialogue"

    # this is actually the users message box
    user_id = Column(db.Integer(), nullable=False)
    # the user to whom the conversation is addressed
    from_user_id = Column(db.Integer())
    # the user who sent the message
    to_user_id = db.Column(db.Integer())
    shared_id = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(255))
    trash = db.Column(db.Boolean, default=False, nullable=False)
    draft = db.Column(db.Boolean, default=False, nullable=False)
    unread = db.Column(db.Boolean, default=False, nullable=False)

    @property
    def last_message(self):
        return (
            Message.query.filter_by(conversation_id=self.id)
            .order_by(Message.id.desc())
            .first()
        )

    @property
    def first_message(self):
        return Message.query.filter_by(conversation_id=self.id).first()

    @property
    def messages(self):
        return Message.query.filter_by(conversation_id=self.id).all()

    @property
    def from_user(self):
        return User.query.filter_by(id=self.from_user_id).first()

    @property
    def to_user(self):
        return User.query.filter_by(id=self.to_user_id).first()
