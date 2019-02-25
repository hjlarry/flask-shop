import random
import string
import datetime

from sqlalchemy.dialects.mysql import TINYINT

from flaskshop.database import Column, Model, db
from flaskshop.constant import VoucherTypeKinds, DiscountValueTypeKinds


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

    def check_available(self, order_total_amount=0, shipping_method_price=0):
        if self.start_date and self.start_date > datetime.datetime.now():
            raise Exception("The voucher code can not use now, please retry later")
        if self.end_date and self.end_date < datetime.datetime.now():
            raise Exception("The voucher code has expired")
        if self.usage_limit and self.usage_limit - self.used < 0:
            raise Exception("This voucher code has been used out")
        if self.type == VoucherTypeKinds.value.value:
            if self.limit and order_total_amount < self.limit:
                raise Exception(
                    "The order total amount is not enough to use this voucher code"
                )
        elif self.type == VoucherTypeKinds.shipping.value:
            if self.limit and shipping_method_price < self.limit:
                raise Exception(
                    "The order shipping price is not enough to use this voucher code"
                )
        return True

    @classmethod
    def get_by_code(cls, code):
        return cls.query.filter_by(code=code).first()

    def get_vouchered_price(self, order_total_amount=0, shipping_method_price=0):
        if self.type == VoucherTypeKinds.value.value:
            return self.get_voucher_from_price(order_total_amount)
        elif self.type == VoucherTypeKinds.shipping.value:
            return self.get_voucher_from_price(shipping_method_price)
        return 0

    def get_voucher_from_price(self, price):
        if self.discount_value_type == DiscountValueTypeKinds.fixed.value:
            return self.discount_value if price > self.discount_value else price
        elif self.discount_value_type == DiscountValueTypeKinds.percent.value:
            return price * self.discount_value


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

