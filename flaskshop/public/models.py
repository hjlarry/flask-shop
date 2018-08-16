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
    top_menu_id = reference_col("menu_menu")
    top_menu = relationship("Menu", foreign_keys=[top_menu_id])
    bottom_menu_id = reference_col("menu_menu")
    bottom_menu = relationship("Menu", foreign_keys=[bottom_menu_id])


class Menu(SurrogatePK, Model):
    __tablename__ = "menu_menu"
    title = Column(db.String(255), nullable=False)


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
    menu_id = reference_col("menu_menu")
    menu = relationship("Menu", backref="items")
    page_id = reference_col("page_page")
    page = relationship("Page")
    parent_id = reference_col("menu_menuitem")

    def __str__(self):
        return self.title

    @property
    def linked_object(self):
        return self.category or self.page  # //TODO collection

    @property
    def get_url(self):
        linked_object = self.linked_object
        return linked_object.get_absolute_url() if linked_object else self.url


MenuItem.parent = relationship("MenuItem", backref="children", remote_side=MenuItem.id)


class Page(SurrogatePK, Model):
    __tablename__ = "page_page"
    title = Column(db.String(255), nullable=False)
    content = Column(db.Text())
    is_visible = Column(db.Boolean(), default=True)

    def get_absolute_url(self):
        return 1
        # return reverse('page:details', kwargs={'slug': self.slug})
