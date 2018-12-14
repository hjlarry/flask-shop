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

user_favorite_product = db.Table(
    "user_favorite_products",
    Column("id", db.Integer(), primary_key=True),
    Column("user_id", db.Integer(), db.ForeignKey("users.id"), primary_key=True),
    Column("product_id", db.Integer(), db.ForeignKey("product_product.id"), primary_key=True),
)


class User(SurrogatePK, Model, UserMixin):
    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False, comment='use`s name')
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    _password = Column('password', db.String(128))
    nick_name = Column(db.String(255))
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    # favor_products = relationship(
    #     "Product", secondary=user_favorite_product, backref="liked_users", lazy='dynamic'
    # )
    orders = relationship('Order', backref="user")
    open_id = Column(db.String(80), index=True)
    session_key = Column(db.String(80), index=True)
    test = Column(db.String(80), comment='haha')

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


class UserAddress(SurrogatePK, Model):
    __tablename__ = "users_address"
    user_id = reference_col("users")
    user = relationship("User", backref="addresses")
    province = Column(db.String(255))
    city = Column(db.String(255))
    district = Column(db.String(255))
    address = Column(db.String(255))
    contact_name = Column(db.String(255))
    contact_phone = Column(db.String(80))

    @property
    def full_address(self):
        return f"{self.province}{self.city}{self.district}{self.address}"

    def __str__(self):
        return self.full_address
