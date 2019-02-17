from flaskshop.database import Column, Model, db


class Voucher(Model):
    __tablename__ = "discount_voucher"
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
    category_id = Column(db.Integer())
    product_id = Column(db.Integer())

    def __str__(self):
        return self.title


class Sale(Model):
    __tablename__ = "discount_sale"
    type = Column(db.String(10))
    title = Column(db.String(255))
    value = Column(db.DECIMAL(10, 2))

    def __str__(self):
        return self.title


class SaleCategory(Model):
    __tablename__ = "discount_sale_categories"
    sale_id = Column(db.Integer())
    category_id = Column(db.Integer())


class SaleProduct(Model):
    __tablename__ = "discount_sale_products"
    sale_id = Column(db.Integer())
    product_id = Column(db.Integer())
