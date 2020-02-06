from flaskshop.database import Column, Model, db


class Message(Model):
    __tablename__ = "conversation_messages"

    conversation_id = Column(db.Integer(), nullable=False)
    user_id = Column(db.Integer(), nullable=False)
    message = Column(db.Text, nullable=False)
