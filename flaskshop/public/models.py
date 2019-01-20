from flask import url_for

from flaskshop.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)


class Site(SurrogatePK, Model):
    __tablename__ = "site_setting"
    header_text = Column(db.String(255), nullable=False)
    description = Column(db.Text())
    top_menu_id = Column(db.Integer())
    bottom_menu_id = Column(db.Integer())

    @property
    def top_menu(self):
        return Menu.get_by_id(self.top_menu_id)

    @property
    def bottom_menu(self):
        return Menu.get_by_id(self.bottom_menu_id)


class Menu(SurrogatePK, Model):
    __tablename__ = "menu_menu"
    title = Column(db.String(255), nullable=False)

    def __str__(self):
        return self.title

    @property
    def items(self):
        return MenuItem.query.filter(MenuItem.menu_id == self.id)


class MenuItem(SurrogatePK, Model):
    __tablename__ = "menu_menuitem"
    title = Column(db.String(255), nullable=False)
    order = Column(db.Integer(), default=0)
    url = Column(db.String(255))
    lft = Column(db.Integer())
    rght = Column(db.Integer())
    level = Column(db.Integer(), default=0)
    category_id = reference_col("product_category")
    category = relationship("Category")
    collection_id = reference_col("product_collection")
    collection = relationship("Collection")
    menu_id = Column(db.Integer())
    page_id = Column(db.Integer())
    parent_id = Column(db.Integer())

    def __str__(self):
        return self.title

    @property
    def menu(self):
        return Menu.get_by_id(self.menu_id)

    @property
    def parent(self):
        return MenuItem.get_by_id(self.parent_id)

    @property
    def children(self):
        return MenuItem.query.filter(MenuItem.parent_id == self.id)

    @property
    def page(self):
        return Page.get_by_id(self.page_id)

    @property
    def linked_object(self):
        return self.category or self.page or self.collection

    @property
    def get_url(self):
        linked_object = self.linked_object
        return linked_object.get_absolute_url() if linked_object else self.url


class Page(SurrogatePK, Model):
    __tablename__ = "page_page"
    title = Column(db.String(255), nullable=False)
    content = Column(db.Text())
    is_visible = Column(db.Boolean(), default=True)

    def get_absolute_url(self):
        return url_for("public.show_page", id=self.id)

    def __str__(self):
        return self.title
