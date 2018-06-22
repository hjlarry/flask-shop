# -*- coding: utf-8 -*-
"""User models."""
from flask_login import UserMixin

from flaskshop.database import Column, Model, SurrogatePK, db, reference_col, relationship
from flaskshop.extensions import bcrypt


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return f'<Role({self.name})>'


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.Binary(128), nullable=True)
    nick_name = Column(db.String(255), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, username, email, password=None, **kwargs):
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        return f'<User({self.username})>'


class UserAddress(SurrogatePK, Model):
    """An address for a user"""

    __tablename__ = 'users_address'
    user_id = reference_col('users', nullable=True)
    province = Column(db.String(255), nullable=True)
    city = Column(db.String(255), nullable=True)
    district = Column(db.String(255), nullable=True)
    address = Column(db.String(255), nullable=True)
    contact_name = Column(db.String(255), nullable=True)
    contact_phone = Column(db.String(80), nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        return f'<Address({self.id})>'


class UserFavoriteProduct(SurrogatePK, Model):
    __tablename__ = 'user_favorite_products'
    user_id = Column(db.Integer())
    product_id = Column(db.Integer())


class UserCart(SurrogatePK, Model):
    __tablename__ = 'cart_items'
    user_id = Column(db.Integer())
    product_sku_id = Column(db.Integer())
    amount = Column(db.Integer())