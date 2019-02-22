import random
import string
import datetime

from sqlalchemy.dialects.mysql import TINYINT

from flaskshop.database import Column, Model, db


class Voucher(Model):
    __tablename__ = "discount_voucher"
    type = Column(TINYINT())
    title = Column(db.String(255))
    code = Column(db.String(16), unique=True)
    usage_limit = Column(db.Integer())
    used = Column(db.Integer(), default=0)
    start_date = Column(db.DateTime())
    end_date = Column(db.DateTime())
    discount_value_type = Column(TINYINT())
    discount_value = Column(db.DECIMAL(10, 2))
    limit = Column(db.DECIMAL(10, 2))
    category_id = Column(db.Integer())
    product_id = Column(db.Integer())

    def __str__(self):
        return self.title

    @classmethod
    def generate_code(cls):
        code = "".join(random.choices(string.ascii_uppercase, k=16))
        exist = cls.query.filter_by(code=code).first()
        if not exist:
            return code
        else:
            return cls.generate_code()

    def check_available(self, order_total_amount=None):
        if self.start_date and self.start_date > datetime.datetime.now():
            raise Exception("The voucher code can not use now, please retry later")
        if self.end_date and self.end_date < datetime.datetime.now():
            raise Exception("The voucher code has expired")
        if self.usage_limit and self.usage_limit - self.used < 0:
            raise Exception("This voucher code has been used out")
        return True


class Sale(Model):
    __tablename__ = "discount_sale"
    discount_value_type = Column(TINYINT())
    title = Column(db.String(255))
    discount_value = Column(db.DECIMAL(10, 2))

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

