from operator import or_
from functools import reduce

from flask_login import UserMixin
from libgravatar import Gravatar
from sqlalchemy.ext.hybrid import hybrid_property

from flaskshop.database import Column, Model, db
from flaskshop.extensions import bcrypt
from flaskshop.constant import Permission


class User(Model, UserMixin):
    __tablename__ = "account_user"
    username = Column(db.String(80), unique=True, nullable=False, comment="user`s name")
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    _password = Column("password", db.String(128))
    nick_name = Column(db.String(255))
    is_active = Column(db.Boolean(), default=False)
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

    @property
    def is_active_human(self):
        return "Y" if self.is_active else "N"

    @property
    def roles(self):
        at_ids = (
            UserRole.query.with_entities(UserRole.role_id)
            .filter_by(user_id=self.id)
            .all()
        )
        return Role.query.filter(Role.id.in_(id for id, in at_ids)).all()

    def delete(self):
        for addr in self.addresses:
            addr.delete()
        return super().delete()

    def can(self, permissions):
        if not self.roles:
            return False
        all_perms = reduce(or_, map(lambda x: x.permissions, self.roles))
        return all_perms & permissions == permissions

    def can_admin(self):
        return self.can(Permission.ADMINISTER)

    def can_edit(self):
        return self.can(Permission.EDITOR)


class UserAddress(Model):
    __tablename__ = "account_address"
    user_id = Column(db.Integer())
    province = Column(db.String(255))
    city = Column(db.String(255))
    district = Column(db.String(255))
    address = Column(db.String(255))
    contact_name = Column(db.String(255))
    contact_phone = Column(db.String(80))

    @property
    def full_address(self):
        return f"{self.province}{self.city}{self.district}<br>{self.address}<br>{self.contact_name}<br>{self.contact_phone}"

    @hybrid_property
    def user(self):
        return User.get_by_id(self.user_id)

    def __str__(self):
        return self.full_address


class Role(Model):
    __tablename__ = "account_role"
    name = Column(db.String(80), unique=True)
    permissions = Column(db.Integer(), default=Permission.LOGIN)


class UserRole(Model):
    __tablename__ = "account_user_role"
    user_id = Column(db.Integer())
    role_id = Column(db.Integer())
