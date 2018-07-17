import ast
from flask import url_for

from flaskshop.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)


class Product(SurrogatePK, Model):
    """A product of the app"""

    __tablename__ = "products"
    title = Column(db.String(255), nullable=False)
    description = Column(db.Text())
    image = Column(db.String(255))
    on_sale = Column(db.Boolean(), default=True)
    rating = Column(db.DECIMAL(8, 2), default=5.0)
    sold_count = Column(db.Integer(), default=0)
    review_count = Column(db.Integer(), default=0)
    price = Column(db.DECIMAL(10, 2))
    category_id = reference_col("product_category")
    category = relationship("Category", backref="products")

    def __repr__(self):
        return f"<Product({self.title})>"

    def __str__(self):
        return self.title

    @property
    def img_url(self):
        if not self.image:
            return None
        if self.image.startswith("http"):
            return self.image
        else:
            return url_for("static", filename=ast.literal_eval(self.image)[0])

    @property
    def img_list(self):
        if not self.image:
            return [""]
        if self.image.startswith("http"):
            return [self.image]
        else:
            return [
                url_for("static", filename=img) for img in ast.literal_eval(self.image)
            ]


class ProductSku(SurrogatePK, Model):
    """sku of this product"""

    __tablename__ = "product_skus"
    title = Column(db.String(255), nullable=False)
    description = Column(db.Text())
    price = Column(db.DECIMAL(10, 2))
    stock = Column(db.Integer())
    product_id = reference_col("products")
    product = relationship("Product", backref="sku")

    def __repr__(self):
        return f"<ProductSku({self.title})>"

    def decrement_stock(self, amount):
        if amount <= 0:
            raise Exception("Can`t low than zero!")
        if amount > self.stock:
            print(amount)
            print(self.stock)
            raise Exception("Not enough stock!")
        self.stock -= amount

    def can_add_to_cart(self, amount):
        if not self.product.on_sale:
            raise Exception("Not On Sale")
        if self.stock == 0:
            raise Exception("Empty Stock")
        if amount > self.stock:
            raise Exception("Not enough stock!")
        return True


class Category(SurrogatePK, Model):
    """a category of a product"""

    __tablename__ = "product_category"
    title = Column(db.String(255), nullable=False)
    parent_id = reference_col("product_category")
    background_img = Column(db.String(255))

    def get_absolute_url(self):
        return 1
        # return reverse('page:details', kwargs={'slug': self.slug})


Category.parent = relationship("Category", backref="children", remote_side=Category.id)
