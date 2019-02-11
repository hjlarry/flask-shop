# -*- coding: utf-8 -*-
"""User models."""
from flask_login import UserMixin
from libgravatar import Gravatar
from sqlalchemy.ext.hybrid import hybrid_property

from flaskshop.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)
from flaskshop.extensions import bcrypt


class User(SurrogatePK, Model, UserMixin):
    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False, comment="use`s name")
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    _password = Column("password", db.String(128))
    nick_name = Column(db.String(255))
    is_active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    open_id = Column(db.String(80), index=True)
    session_key = Column(db.String(80), index=True)

    def __init__(self, username, email, password, **kwargs):
        super().__init__(username=username, email=email, password=password, **kwargs)

    def __str__(self):
        return self.username

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = bcrypt.generate_password_hash(value)

    @property
    def avatar(self):
        return Gravatar(self.email).get_image()

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def addresses(self):
        return UserAddress.query.filter_by(user_id=self.id)


class UserAddress(SurrogatePK, Model):
    __tablename__ = "users_address"
    user_id = Column(db.Integer())
    province = Column(db.String(255))
    city = Column(db.String(255))
    district = Column(db.String(255))
    address = Column(db.String(255))
    contact_name = Column(db.String(255))
    contact_phone = Column(db.String(80))

    @property
    def full_address(self):
        return f"{self.province}{self.city}{self.district}{self.address}"

    @hybrid_property
    def user(self):
        return User.get_by_id(self.user_id)

    def __str__(self):
        return self.full_address
