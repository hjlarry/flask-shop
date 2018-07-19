import string
import random
import datetime

from flaskshop.constant import TYPE_FIXED
from flaskshop.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)


class UserCart(SurrogatePK, Model):
    __tablename__ = "cart_items"
    # user_id = reference_col("users")
    # user = relationship("User", backref="cart_items")
    product_sku_id = reference_col("product_skus")
    product_sku = relationship("ProductSku")
    amount = Column(db.Integer())

    def release(self, amount):
        """when submit order, release cart items in order"""
        self.amount -= amount
        if self.amount <= 0:
            self.delete()


class Cart(SurrogatePK, Model):
    __tablename__ = "checkout_cart"
    user_id = reference_col("users")
    user = relationship("User", backref="cart_items")
    token = Column(db.String(255))
    voucher_code = Column(db.String(255))
    quantity = Column(db.Integer())


class CartLine(SurrogatePK, Model):
    __tablename__ = "checkout_cartline"
    cart_id = reference_col("checkout_cart")
    cart = relationship("Cart", backref="cart_lines")
    quantity = Column(db.Integer())
    variant_id = reference_col("product_variant")
    variant = relationship("ProductVariant")


class CouponCode(SurrogatePK, Model):
    __tablename__ = "coupon_codes"
    title = Column(db.String(255), nullable=False)
    code = Column(db.String(255), unique=True, nullable=False)
    type = Column(db.String(255), nullable=False)
    value = Column(db.String(255), nullable=False)
    total = Column(db.Integer())
    used = Column(db.Integer(), default=0)
    min_amount = Column(db.DECIMAL(10, 2))
    not_before = Column(db.DateTime())
    not_after = Column(db.DateTime())
    enabled = Column(db.Boolean(), default=True)

    @property
    def description(self):
        full = ''
        if self.min_amount > 0:
            full = '满' + str(self.min_amount)
        if self.type == TYPE_FIXED:
            return full + '减' + str(self.value)
        return full + '优惠' + str(self.value).replace('.00', '') + '%'

    @classmethod
    def generate_code(cls):
        code = ''.join(random.choices(string.ascii_uppercase, k=16))
        exist = cls.query.filter_by(code=code).first()
        if not exist:
            return code
        else:
            return cls.generate_code()

    def check_available(self, order_total_amount=None):
        if not self.enabled:
            raise Exception('This code can not use by system')
        if self.total - self.used < 0:
            raise Exception('The coupon has been redeemed')
        if self.not_before and self.not_before > datetime.datetime.now():
            raise Exception('The coupon can not use now, please retry later')
        if self.not_after and self.not_after < datetime.datetime.now():
            raise Exception('The coupon has expired')
        if order_total_amount and order_total_amount < self.min_amount:
            raise Exception('The order amount does not meet the minimum amount of the coupon')
        return True

    def get_adjusted_price(self, order_total_amount):
        if self.type == TYPE_FIXED:
            return max(0.01, float(order_total_amount) - float(self.value))
        return float(order_total_amount) * (100 - float(self.value)) / 100
