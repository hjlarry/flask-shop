from flask import flash
from sqlalchemy.dialects.mysql import BOOLEAN
from flask_login import current_user

from flaskshop.constant import DiscountValueTypeKinds
from flaskshop.database import Column, Model, db
from flaskshop.product.models import ProductVariant
from flaskshop.discount.models import Voucher
from flaskshop.corelib.mc import cache
from flaskshop.corelib.mc import rdb

MC_KEY_CART_BY_USER = "checkout:cart:user_id:{}"


class Cart(Model):
    __tablename__ = "checkout_cart"
    user_id = Column(db.Integer())
    voucher_code = Column(db.String(255))
    quantity = Column(db.Integer())
    shipping_address_id = Column(db.Integer())
    shipping_method_id = Column(db.Integer())

    @property
    def subtotal(self):
        return sum(line.subtotal for line in self)

    @property
    def total(self):
        return self.subtotal + self.shipping_method_price - self.discount_amount

    @property
    def discount_amount(self):
        return self.voucher.get_vouchered_price(self) if self.voucher_code else 0

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
        variant = ProductVariant.get_by_id(variant_id)
        result, msg = variant.check_enough_stock(quantity)
        if result is False:
            flash(msg, "warning")
            return
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

    def get_product_price(self, product_id):
        price = 0
        for line in self:
            if line.product.id == product_id:
                price += line.subtotal
        return price

    def get_category_price(self, category_id):
        price = 0
        for line in self:
            if line.category.id == category_id:
                price += line.subtotal
        return price

    @property
    def is_shipping_required(self):
        return any(line.is_shipping_required for line in self)

    @property
    def shipping_method(self):
        return ShippingMethod.get_by_id(self.shipping_method_id)

    @property
    def shipping_method_price(self):
        if self.shipping_method:
            return self.shipping_method.price
        return 0

    @property
    def voucher(self):
        if self.voucher_code:
            return Voucher.get_by_code(self.voucher_code)
        return None

    def __repr__(self):
        return f"Cart(quantity={self.quantity})"

    def __iter__(self):
        return iter(self.lines)

    def __len__(self):
        return len(self.lines)

    def update_quantity(self):
        self.quantity = sum(line.quantity for line in self)
        if self.quantity == 0:
            self.delete()
        else:
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
    def category(self):
        return self.product.category

    @property
    def subtotal(self):
        return self.variant.price * self.quantity


class ShippingMethod(Model):
    __tablename__ = "checkout_shippingmethod"
    title = Column(db.String(255), nullable=False)
    price = Column(db.DECIMAL(10, 2))

    def __str__(self):
        return self.title + "   $" + str(self.price)

    @property
    def price_human(self):
        return "$" + str(self.price)
