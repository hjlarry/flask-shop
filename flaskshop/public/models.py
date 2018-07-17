from flaskshop.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)


class Site(SurrogatePK, Model):
    """Site config of the app"""

    __tablename__ = "site_setting"
    header_text = Column(db.String(255), nullable=False)
    description = Column(db.Text())
    top_menu_id = reference_col("menu_menu")
    top_menu = relationship("Menu", foreign_keys=[top_menu_id])
    bottom_menu_id = reference_col("menu_menu")
    bottom_menu = relationship("Menu", foreign_keys=[bottom_menu_id])

    def __repr__(self):
        return f"<Site({self.header_text})>"


class Menu(SurrogatePK, Model):
    """Menu config of the app"""

    __tablename__ = "menu_menu"
    title = Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Menu({self.title})>"


class MenuItem(SurrogatePK, Model):
    """an item of a menu"""

    __tablename__ = "menu_menuitem"
    title = Column(db.String(255), nullable=False)
    order = Column(db.Integer(), default=0)
    url = Column(db.String(255))
    lft = Column(db.Integer())
    rght = Column(db.Integer())
    level = Column(db.Integer(), default=0)
    category_id = reference_col("product_category")
    category = relationship("Category")
    menu_id = reference_col("menu_menu")
    menu = relationship("Menu", backref="menu_items")
    page_id = reference_col("page_page")
    parent_id = reference_col("menu_menuitem")

    def __repr__(self):
        return f"<MenuItem({self.title})>"


MenuItem.parent = relationship("MenuItem", backref="children", remote_side=MenuItem.id)


class Page(SurrogatePK, Model):
    """a page of the site"""

    __tablename__ = "page_page"
    title = Column(db.String(255), nullable=False)
    content = Column(db.Text())
    is_visible = Column(db.Boolean(), default=True)

    def __repr__(self):
        return f"<Page({self.title})>"
