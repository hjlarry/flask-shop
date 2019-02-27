import random
import string
from datetime import datetime
from decimal import Decimal

from sqlalchemy.dialects.mysql import TINYINT

from flaskshop.database import Column, Model, db
from flaskshop.constant import VoucherTypeKinds, DiscountValueTypeKinds
from flaskshop.product.models import Product, Category


class Voucher(Model):
    __tablename__ = "discount_voucher"
    type = Column(TINYINT())
    title = Column(db.String(255))
    code = Column(db.String(16), unique=True)
    usage_limit = Column(db.Integer())
    used = Column(db.Integer(), default=0)
    start_date = Column(db.Date())
    end_date = Column(db.Date())
    discount_value_type = Column(TINYINT())
    discount_value = Column(db.DECIMAL(10, 2))
    limit = Column(db.DECIMAL(10, 2))
    category_id = Column(db.Integer())
    product_id = Column(db.Integer())

    def __str__(self):
        return self.title

    @property
    def type_label(self):
        return VoucherTypeKinds(int(self.type)).name

    @property
    def discount_value_type_label(self):
        return DiscountValueTypeKinds(int(self.discount_value_type)).name

    @property
    def validity_period(self):
        return (
            datetime.strftime(self.start_date, "%m/%d/%Y")
            + " - "
            + datetime.strftime(self.end_date, "%m/%d/%Y")
        )

    @classmethod
    def generate_code(cls):
        code = "".join(random.choices(string.ascii_uppercase, k=16))
        exist = cls.query.filter_by(code=code).first()
        if not exist:
            return code
        else:
            return cls.generate_code()

    def check_available(self, cart=None):
        if self.start_date and self.start_date > datetime.now():
            raise Exception("The voucher code can not use now, please retry later")
        if self.end_date and self.end_date < datetime.now():
            raise Exception("The voucher code has expired")
        if self.usage_limit and self.usage_limit - self.used < 0:
            raise Exception("This voucher code has been used out")
        if cart:
            self.check_available_by_cart(cart)

        return True

    def check_available_by_cart(self, cart):
        if self.type == VoucherTypeKinds.value.value:
            if self.limit and cart.subtotal < self.limit:
                raise Exception(
                    f"The order total amount is not enough({self.limit}) to use this voucher code"
                )
        elif self.type == VoucherTypeKinds.shipping.value:
            if self.limit and cart.shipping_method_price < self.limit:
                raise Exception(
                    f"The order shipping price is not enough({self.limit}) to use this voucher code"
                )
        elif self.type == VoucherTypeKinds.product.value:
            product = Product.get_by_id(self.product_id)
            # got any product in cart, should be zero
            if cart.get_product_price(self.product_id) == 0:
                raise Exception(f"This Voucher Code should be used for {product.title}")
            if self.limit and cart.get_product_price(self.product_id) < self.limit:
                raise Exception(
                    f"The product {product.title} total amount is not enough({self.limit}) to use this voucher code"
                )
        elif self.type == VoucherTypeKinds.category.value:
            category = Category.get_by_id(self.category_id)
            if cart.get_category_price(self.category_id) == 0:
                raise Exception(
                    f"This Voucher Code should be used for {category.title}"
                )
            if self.limit and cart.get_category_price(self.category_id) < self.limit:
                raise Exception(
                    f"The category {category.title} total amount is not enough({self.limit}) to use this voucher code"
                )

    @classmethod
    def get_by_code(cls, code):
        return cls.query.filter_by(code=code).first()

    def get_vouchered_price(self, cart):
        if self.type == VoucherTypeKinds.value.value:
            return self.get_voucher_from_price(cart.subtotal)
        elif self.type == VoucherTypeKinds.shipping.value:
            return self.get_voucher_from_price(cart.shipping_method_price)
        elif self.type == VoucherTypeKinds.product.value:
            return self.get_voucher_from_price(cart.get_product_price(self.product_id))
        elif self.type == VoucherTypeKinds.category.value:
            return self.get_voucher_from_price(
                cart.get_category_price(self.category_id)
            )
        return 0

    def get_voucher_from_price(self, price):
        if self.discount_value_type == DiscountValueTypeKinds.fixed.value:
            return self.discount_value if price > self.discount_value else price
        elif self.discount_value_type == DiscountValueTypeKinds.percent.value:
            price = price * self.discount_value / 100
            return Decimal(price).quantize(Decimal("0.00"))


class Sale(Model):
    __tablename__ = "discount_sale"
    discount_value_type = Column(TINYINT())
    title = Column(db.String(255))
    discount_value = Column(db.DECIMAL(10, 2))

    def __str__(self):
        return self.title

    @classmethod
    def get_discounted_price(cls, product):
        sale_product = SaleProduct.query.filter_by(product_id=product.id).first()
        if sale_product:
            sale = Sale.get_by_id(sale_product.sale_id)
        else:
            sale_category = SaleCategory.query.filter_by(
                category_id=product.category.id
            ).first()
            sale = Sale.get_by_id(sale_category.sale_id) if sale_category else None
        if sale is None:
            return 0
        if sale.discount_value_type == DiscountValueTypeKinds.fixed.value:
            return sale.discount_value
        elif sale.discount_value_type == DiscountValueTypeKinds.percent.value:
            price = product.basic_price * sale.discount_value / 100
            return Decimal(price).quantize(Decimal("0.00"))


class SaleCategory(Model):
    __tablename__ = "discount_sale_categories"
    sale_id = Column(db.Integer())
    category_id = Column(db.Integer())


class SaleProduct(Model):
    __tablename__ = "discount_sale_products"
    sale_id = Column(db.Integer())
    product_id = Column(db.Integer())

