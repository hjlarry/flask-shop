from flaskshop.database import Column, Model, SurrogatePK, db, reference_col, relationship


class Product(SurrogatePK, Model):
    """A product of the app"""

    __tablename__ = 'products'
    title = Column(db.String(255), nullable=False)
    description = Column(db.Text())
    image = Column(db.String(255))
    on_sale = Column(db.Boolean(), default=True)
    rating = Column(db.Float(8, 2), default=5.0)
    sold_count = Column(db.Integer(), default=0)
    review_count = Column(db.Integer(), default=0)
    price = Column(db.DECIMAL(10, 2))

    def __init__(self, title, **kwargs):
        db.Model.__init__(self, title=title, **kwargs)

    def __repr__(self):
        return f'<Product({self.title})>'


class ProductSku(SurrogatePK, Model):
    """sku of this product"""

    __tablename__ = 'product_skus'
    title = Column(db.String(255), nullable=False)
    description = Column(db.Text())
    price = Column(db.DECIMAL(10, 2))
    stock = Column(db.Integer())
    product_id = reference_col('products')

    def __init__(self, title, **kwargs):
        db.Model.__init__(self, title=title, **kwargs)

    def __repr__(self):
        return f'<ProductSku({self.title})>'
