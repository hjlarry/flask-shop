from flaskshop.database import Column, Model, SurrogatePK, db, reference_col, relationship


sale_categories = db.Table(
    "discount_sale_categories",
    Column("id", db.Integer(), primary_key=True, autoincrement=True),
    Column(
        "sale_id",
        db.Integer(),
        db.ForeignKey("discount_sale.id"),
        primary_key=True,
    ),
    Column(
        "category_id",
        db.Integer(),
        db.ForeignKey("product_category.id"),
        primary_key=True,
    ),
)

sale_products = db.Table(
    "discount_sale_products",
    Column("id", db.Integer(), primary_key=True, autoincrement=True),
    Column(
        "sale_id",
        db.Integer(),
        db.ForeignKey("discount_sale.id"),
        primary_key=True,
    ),
    Column(
        "product_id",
        db.Integer(),
        db.ForeignKey("product_product.id"),
        primary_key=True,
    ),
)



class Voucher(SurrogatePK, Model):
    __tablename__ = 'discount_voucher'
    type = Column(db.String(20))
    title = Column(db.String(255))
    code = Column(db.String(12))
    usage_limit = Column(db.Integer())
    used = Column(db.Integer())
    start_date = Column(db.DateTime())
    end_date = Column(db.DateTime())
    discount_value_type = Column(db.String(12))
    discount_value = Column(db.DECIMAL(10, 2))
    apply_to = Column(db.String(20))
    limit = Column(db.DECIMAL(10, 2))
    category_id = reference_col('product_category')
    product_id = reference_col('product_product')
    product = relationship('Product', backref="discounts")


class Sale(SurrogatePK, Model):
    __tablename__ = 'discount_sale'
    type = Column(db.String(10))
    title = Column(db.String(255))
    value = Column(db.DECIMAL(10, 2))
    products = relationship(
        "Product", secondary=sale_products, backref="sales", lazy='dynamic'
    )

