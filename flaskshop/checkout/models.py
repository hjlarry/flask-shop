import string
import random
import datetime
from sqlalchemy.dialects.mysql import BOOLEAN
from flask_login import current_user

from flaskshop.constant import DISCOUNT_VALUE_FIXED
from flaskshop.database import Column, Model, db
from flaskshop.account.models import UserAddress
from flaskshop.product.models import ProductVariant
from flaskshop.corelib.mc import cache
from flaskshop.corelib.mc import rdb

MC_KEY_CART_BY_USER = "checkout:cart:user_id:{}"


class Cart(Model):
    __tablename__ = "checkout_cart"
    user_id = Column(db.Integer())
    token = Column(db.String(255))
    voucher_code = Column(db.String(255))
    quantity = Column(db.Integer())
    shipping_address_id = Column(db.Integer())

    @property
    def total(self):
        # TODO discount and tax
        subtotal = (line.subtotal for line in self.lines)
        return sum(subtotal)

    @property
    def address(self):
        return UserAddress.get_by_id(self.shipping_address_id)

    @property
    def lines(self):
        return CartLine.query.filter(CartLine.cart_id == self.id).all()

    @classmethod
    @cache(MC_KEY_CART_BY_USER.format("{user_id}"))
    def get_cart_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def get_current_user_cart(cls):
        if current_user.is_authenticated:
            cart = cls.get_cart_by_user_id(current_user.id)
        else:
            cart = None
        return cart

    @classmethod
    def add_to_currentuser_cart(cls, quantity, variant_id):
        cart = cls.get_current_user_cart()
        if cart:
            cart.quantity += quantity
            cart.save()
        else:
            cart = cls.create(user_id=current_user.id, quantity=quantity)
        line = CartLine.query.filter_by(cart_id=cart.id, variant_id=variant_id).first()
        if line:
            quantity += line.quantity
            line.update(quantity=quantity)
        else:
            CartLine.create(variant_id=variant_id, quantity=quantity, cart_id=cart.id)

    @property
    def is_shipping_required(self):
        return any(line.is_shipping_required for line in self)

    def __repr__(self):
        return f"Cart(quantity={self.quantity})"

    def __iter__(self):
        return iter(self.lines)

    def __len__(self):
        return len(self.lines)

    def update_quantity(self):
        self.quantity = sum(line.quantity for line in self)
        self.save()
        return self.quantity

    @classmethod
    def __flush_insert_event__(cls, target):
        rdb.delete(MC_KEY_CART_BY_USER.format(current_user.id))

    @classmethod
    def __flush_after_update_event__(cls, target):
        super().__flush_after_update_event__(target)
        rdb.delete(MC_KEY_CART_BY_USER.format(current_user.id))

    @classmethod
    def __flush_delete_event__(cls, target):
        super().__flush_delete_event__(target)
        rdb.delete(MC_KEY_CART_BY_USER.format(current_user.id))


class CartLine(Model):
    __tablename__ = "checkout_cartline"
    cart_id = Column(db.Integer())
    quantity = Column(db.Integer())
    variant_id = Column(db.Integer())

    def __repr__(self):
        return f"CartLine(variant={self.variant}, quantity={self.quantity})"

    @property
    def is_shipping_required(self):
        return self.variant.is_shipping_required

    @property
    def variant(self):
        return ProductVariant.get_by_id(self.variant_id)

    @property
    def product(self):
        return self.variant.product

    @property
    def subtotal(self):
        return self.variant.price * self.quantity


class ShippingMethod(Model):
    __tablename__ = "checkout_shippingmethod"
    title = Column(db.String(255), nullable=False)
    price = Column(db.DECIMAL(10, 2))

    def __str__(self):
        return self.title + "   $" + str(self.price)


class CouponCode(Model):
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
    enabled = Column(BOOLEAN(), default=True)

    @property
    def description(self):
        full = ""
        if self.min_amount > 0:
            full = "满" + str(self.min_amount)
        if self.type == DISCOUNT_VALUE_FIXED:
            return full + "减" + str(self.value)
        return full + "优惠" + str(self.value).replace(".00", "") + "%"

    @classmethod
    def generate_code(cls):
        code = "".join(random.choices(string.ascii_uppercase, k=16))
        exist = cls.query.filter_by(code=code).first()
        if not exist:
            return code
        else:
            return cls.generate_code()

    def check_available(self, order_total_amount=None):
        if not self.enabled:
            raise Exception("This code can not use by system")
        if self.total - self.used < 0:
            raise Exception("The coupon has been redeemed")
        if self.not_before and self.not_before > datetime.datetime.now():
            raise Exception("The coupon can not use now, please retry later")
        if self.not_after and self.not_after < datetime.datetime.now():
            raise Exception("The coupon has expired")
        if order_total_amount and order_total_amount < self.min_amount:
            raise Exception(
                "The order amount does not meet the minimum amount of the coupon"
            )
        return True

    def get_adjusted_price(self, order_total_amount):
        if self.type == DISCOUNT_VALUE_FIXED:
            return max(0.01, float(order_total_amount) - float(self.value))
        return float(order_total_amount) * (100 - float(self.value)) / 100
