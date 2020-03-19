from flask import url_for, request

from flaskshop.database import Column, Model, db
from flaskshop.constant import SettingValueType


class DashboardMenu(Model):
    __tablename__ = "management_dashboard"
    title = Column(db.String(255), nullable=False)
    order = Column(db.Integer(), default=0)
    endpoint = Column(db.String(255))
    icon_cls = Column(db.String(255))
    parent_id = Column(db.Integer(), default=0)

    def __str__(self):
        return self.title

    @property
    def children(self):
        return DashboardMenu.query.filter(DashboardMenu.parent_id == self.id).all()

    @classmethod
    def first_level_items(cls):
        return cls.query.filter(cls.parent_id == 0).order_by("order").all()

    def is_active(self):
        if self.endpoint and self.endpoint in request.path:
            return True
        if any((child.is_active() for child in self.children)):
            return True
        return False

    def get_url(self):
        if self.children:
            return "#"
        if self.endpoint:
            return url_for("dashboard." + self.endpoint)


class Setting(Model):
    __tablename__ = "management_setting"
    id = None
    key = Column(db.String(255), primary_key=True)
    value = Column(db.PickleType, nullable=False)
    name = Column(db.String(255), nullable=False)
    description = Column(db.Text, nullable=False)
    value_type =  Column(db.Enum(SettingValueType), nullable=False)
    extra = Column(db.PickleType)