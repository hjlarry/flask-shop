# -*- coding: utf-8 -*-
"""User models."""
from flask_login import UserMixin

from flaskshop.database import Column, Model, SurrogatePK, db, reference_col, relationship
from flaskshop.extensions import bcrypt

user_favorite_product = db.Table(
    'user_favorite_products',
    Column('user_id', db.Integer(), db.ForeignKey('users.id'), primary_key=True),
    Column('product_id', db.Integer(), db.ForeignKey('products.id'), primary_key=True)
)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.Binary(128))
    nick_name = Column(db.String(255))
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    favor_products = relationship('Product', secondary=user_favorite_product, backref='liked_users')

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
    user_id = reference_col('users')
    user = relationship('User', backref='addresses')
    province = Column(db.String(255))
    city = Column(db.String(255))
    district = Column(db.String(255))
    address = Column(db.String(255))
    contact_name = Column(db.String(255))
    contact_phone = Column(db.String(80))

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        return f'<Address({self.id})>'


class UserCart(SurrogatePK, Model):
    """A cart of a user"""

    __tablename__ = 'cart_items'
    user_id = reference_col('users')
    user = relationship('User', backref='cart_items')
    product_sku_id = reference_col('product_skus')
    product_sku = relationship('ProductSku')
    amount = Column(db.Integer())

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        return f'<Cart({self.id})>'


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col('users')
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return f'<Role({self.name})>'
