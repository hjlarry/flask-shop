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
    rating = Column(db.Float(8, 2), default=5.0)
    sold_count = Column(db.Integer(), default=0)
    review_count = Column(db.Integer(), default=0)
    price = Column(db.DECIMAL(10, 2))

    def __repr__(self):
        return f"<Product({self.title})>"


class ProductSku(SurrogatePK, Model):
    """sku of this product"""

    __tablename__ = "product_skus"
    title = Column(db.String(255), nullable=False)
    description = Column(db.Text())
    price = Column(db.DECIMAL(10, 2))
    stock = Column(db.Integer())
    product_id = reference_col("products")
    product = relationship('Product', backref='sku', cascade="all,delete")

    def __repr__(self):
        return f"<ProductSku({self.title})>"

    def decrement_stock(self, amount):
        if amount <= 0:
            raise Exception('Can`t low than zero!')
        if amount > self.stock:
            print(amount)
            print(self.stock)
            raise Exception('Not enough stock!')
        self.stock -= amount

    def can_add_to_cart(self, amount):
        if not self.product.on_sale:
            raise Exception('Not On Sale')
        if self.stock == 0:
            raise Exception('Empty Stock')
        if amount > self.stock:
            raise Exception('Not enough stock!')
        return True
