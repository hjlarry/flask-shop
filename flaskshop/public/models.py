from flask import url_for

from flaskshop.database import Column, Model, db
from flaskshop.corelib.mc import cache, rdb
from flaskshop.corelib.db import PropsItem
from flaskshop.settings import Config

MC_KEY_MENU_ITEMS = "public:site:{}:{}"
MC_KEY_MENU_ITEM_CHILDREN = "public:menuitem:{}:children"
MC_KEY_PAGE_ID = "public:page:{}"


class MenuItem(Model):
    __tablename__ = "public_menuitem"
    title = Column(db.String(255), nullable=False)
    order = Column(db.Integer(), default=0)
    url_ = Column("url", db.String(255))
    category_id = Column(db.Integer(), default=0)
    collection_id = Column(db.Integer(), default=0)
    position = Column(db.Integer(), default=0)  # item在site中的位置, 1是top，2是bottom
    page_id = Column(db.Integer(), default=0)
    parent_id = Column(db.Integer(), default=0)

    def __str__(self):
        return self.title

    @property
    def parent(self):
        return MenuItem.get_by_id(self.parent_id)

    @property
    @cache(MC_KEY_MENU_ITEM_CHILDREN.format("{self.id}"))
    def children(self):
        return (
            MenuItem.query.filter(MenuItem.parent_id == self.id).order_by("order").all()
        )

    @property
    def linked_object_url(self):
        if self.page_id:
            return Page.get_by_id(self.page_id).url
        elif self.category_id:
            return url_for("product.show_category", id=self.category_id)
        elif self.collection_id:
            return url_for("product.show_collection", id=self.collection_id)

    @property
    def url(self):
        return self.url_ if self.url_ else self.linked_object_url

    @classmethod
    def first_level_items(cls):
        return cls.query.filter(cls.parent_id == 0).order_by("order").all()


class Page(Model):
    __tablename__ = "public_page"
    title = Column(db.String(255), nullable=False)
    slug = Column(db.String(255))
    content = Column(db.Text())
    is_visible = Column(db.Boolean(), default=True)
    if Config.USE_REDIS:
        content = PropsItem("content", "")

    def get_absolute_url(self):
        identity = self.slug or self.id
        return url_for("public.show_page", identity=identity)

    @classmethod
    @cache(MC_KEY_PAGE_ID.format("{identity}"))
    def get_by_identity(cls, identity):
        try:
            int(identity)
        except ValueError:
            return Page.query.filter(Page.slug == identity).first()
        return Page.get_by_id(identity)

    @property
    def url(self):
        return self.get_absolute_url()

    def __str__(self):
        return self.title

    @classmethod
    def __flush_after_update_event__(cls, target):
        super().__flush_after_update_event__(target)
        rdb.delete(MC_KEY_PAGE_ID.format(target.id))
        rdb.delete(MC_KEY_PAGE_ID.format(target.slug))
