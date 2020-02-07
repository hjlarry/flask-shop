from flaskshop.database import Column, Model, db


class Message(Model):
    __tablename__ = "conversation_messages"

    conversation_id = Column(db.Integer(), nullable=False)
    user_id = Column(db.Integer(), nullable=False)
    message = Column(db.Text, nullable=False)


class Conversation(Model):
    __tablename__ = "conversation_dialogue"

    # this is actually the users message box
    user_id = Column(db.Integer(), nullable=False)
    # the user to whom the conversation is addressed
    from_user_id = Column(db.Integer())
    # the user who sent the message
    to_user_id = db.Column(db.Integer())
    shared_id = db.Column(db.Integer(), unique=True, nullable=False)
    subject = db.Column(db.String(255))
    trash = db.Column(db.Boolean, default=False, nullable=False)
    draft = db.Column(db.Boolean, default=False, nullable=False)
    unread = db.Column(db.Boolean, default=False, nullable=False)