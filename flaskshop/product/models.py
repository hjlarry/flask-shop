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
    __tablename__ = "product_product"
    title = Column(db.String(255), nullable=False)
    description = Column(db.Text())
    image = Column(db.String(255))
    on_sale = Column(db.Boolean(), default=True)
    rating = Column(db.DECIMAL(8, 2), default=5.0)
    sold_count = Column(db.Integer(), default=0)
    review_count = Column(db.Integer(), default=0)
    price = Column(db.DECIMAL(10, 2))
    category_id = reference_col("product_category")
    category = relationship("Category", backref="product_product")
    is_featured = Column(db.Boolean(), default=False)


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

    @property
    def get_absolute_url(self):
        return url_for('product.show', id=self.id)


class ProductSku(SurrogatePK, Model):
    __tablename__ = "product_skus"
    title = Column(db.String(255), nullable=False)
    description = Column(db.Text())
    price = Column(db.DECIMAL(10, 2))
    stock = Column(db.Integer())
    product_id = reference_col("product_product")
    product = relationship("Product", backref="sku")


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
    __tablename__ = "product_category"
    title = Column(db.String(255), nullable=False)
    parent_id = reference_col("product_category")
    background_img = Column(db.String(255))

    def get_absolute_url(self):
        return 1


Category.parent = relationship("Category", backref="children", remote_side=Category.id)


class ProductType(SurrogatePK, Model):
    __tablename__ = "product_producttype"
    title = Column(db.String(255), nullable=False)
    has_variants = Column(db.Boolean(), default=True)
    is_shipping_required = Column(db.Boolean(), default=False)


class ProductVariant(SurrogatePK, Model):
    __tablename__ = "product_variant"
    sku = Column(db.String(32), unique=True)
    title = Column(db.String(255), nullable=False)
    price_override = Column(db.DECIMAL(10, 2))
    quantity = Column(db.Integer())


class ProductAttribute(SurrogatePK, Model):
    __tablename__ = "product_productattribute"
    title = Column(db.String(255), nullable=False)



class ProductImage(SurrogatePK, Model):
    __tablename__ = "product_productimage"
    image = Column(db.String(255))
    order = Column(db.Integer())
    product_id = reference_col("product_product")
    product = relationship("Product", backref="images")