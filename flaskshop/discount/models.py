import random
import string
from datetime import datetime
from decimal import Decimal

from sqlalchemy.dialects.mysql import TINYINT

from flaskshop.corelib.mc import cache, rdb
from flaskshop.database import Column, Model, db
from flaskshop.constant import VoucherTypeKinds, DiscountValueTypeKinds
from flaskshop.product.models import Product, Category, MC_KEY_PRODUCT_DISCOUNT_PRICE


MC_KEY_SALE_PRODUCT_IDS = "discount:sale:{}:product_ids"


class Voucher(Model):
    __tablename__ = "discount_voucher"
    type_ = Column("type", TINYINT())
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
    def type_human(self):
        return VoucherTypeKinds(int(self.type_)).name

    @property
    def discount_value_type_human(self):
        return DiscountValueTypeKinds(int(self.discount_value_type)).name

    @property
    def validity_period(self):
        if self.start_date and self.end_date:
            return (
                datetime.strftime(self.start_date, "%m/%d/%Y")
                + " - "
                + datetime.strftime(self.end_date, "%m/%d/%Y")
            )
        return ""

    @classmethod
    def generate_code(cls):
        code = "".join(random.choices(string.ascii_uppercase, k=16))
        exist = cls.query.filter_by(code=code).first()
        if not exist:
            return code
        else:
            return cls.generate_code()

    def check_available(self, cart=None):
        if self.start_date and self.start_date > datetime.date(datetime.now()):
            raise Exception("The voucher code can not use now, please retry later")
        if self.end_date and self.end_date < datetime.date(datetime.now()):
            raise Exception("The voucher code has expired")
        if self.usage_limit and self.usage_limit - self.used < 0:
            raise Exception("This voucher code has been used out")
        if cart:
            self.check_available_by_cart(cart)

        return True

    def check_available_by_cart(self, cart):
        if self.type_ == VoucherTypeKinds.value.value:
            if self.limit and cart.subtotal < self.limit:
                raise Exception(
                    f"The order total amount is not enough({self.limit}) to use this voucher code"
                )
        elif self.type_ == VoucherTypeKinds.shipping.value:
            if self.limit and cart.shipping_method_price < self.limit:
                raise Exception(
                    f"The order shipping price is not enough({self.limit}) to use this voucher code"
                )
        elif self.type_ == VoucherTypeKinds.product.value:
            product = Product.get_by_id(self.product_id)
            # got any product in cart, should be zero
            if cart.get_product_price(self.product_id) == 0:
                raise Exception(f"This Voucher Code should be used for {product.title}")
            if self.limit and cart.get_product_price(self.product_id) < self.limit:
                raise Exception(
                    f"The product {product.title} total amount is not enough({self.limit}) to use this voucher code"
                )
        elif self.type_ == VoucherTypeKinds.category.value:
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
        if self.type_ == VoucherTypeKinds.value.value:
            return self.get_voucher_from_price(cart.subtotal)
        elif self.type_ == VoucherTypeKinds.shipping.value:
            return self.get_voucher_from_price(cart.shipping_method_price)
        elif self.type_ == VoucherTypeKinds.product.value:
            return self.get_voucher_from_price(cart.get_product_price(self.product_id))
        elif self.type_ == VoucherTypeKinds.category.value:
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

    @property
    def discount_value_type_label(self):
        return DiscountValueTypeKinds(int(self.discount_value_type)).name

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

    @property
    def categories(self):
        at_ids = (
            SaleCategory.query.with_entities(SaleCategory.category_id)
            .filter(SaleCategory.sale_id == self.id)
            .all()
        )
        return Category.query.filter(Category.id.in_(id for id, in at_ids)).all()

    @property
    def products_ids(self):
        return (
            SaleProduct.query.with_entities(SaleProduct.product_id)
            .filter(SaleProduct.sale_id == self.id)
            .all()
        )

    @property
    def products(self):
        return Product.query.filter(
            Product.id.in_(id for id, in self.products_ids)
        ).all()

    def update_categories(self, category_ids):
        origin_ids = (
            SaleCategory.query.with_entities(SaleCategory.category_id)
            .filter_by(sale_id=self.id)
            .all()
        )
        origin_ids = set(i for i, in origin_ids)
        new_attrs = set(int(i) for i in category_ids)
        need_del = origin_ids - new_attrs
        need_add = new_attrs - origin_ids
        for id in need_del:
            SaleCategory.query.filter_by(
                sale_id=self.id, category_id=id
            ).first().delete(commit=False)
        for id in need_add:
            new = SaleCategory(sale_id=self.id, category_id=id)
            db.session.add(new)
        db.session.commit()

    def update_products(self, product_ids):
        origin_ids = (
            SaleProduct.query.with_entities(SaleProduct.product_id)
            .filter_by(sale_id=self.id)
            .all()
        )
        origin_ids = set(i for i, in origin_ids)
        new_attrs = set(int(i) for i in product_ids)
        need_del = origin_ids - new_attrs
        need_add = new_attrs - origin_ids
        for id in need_del:
            SaleProduct.query.filter_by(sale_id=self.id, product_id=id).first().delete(
                commit=False
            )
        for id in need_add:
            new = SaleProduct(sale_id=self.id, product_id=id)
            db.session.add(new)
        db.session.commit()

    @staticmethod
    def clear_mc(target):
        # when update sales, need to update product discounts
        # for (id,) in target.products_ids:
        #     rdb.delete(MC_KEY_PRODUCT_DISCOUNT_PRICE.format(id))

        # need to process so many states, category update etc.. so delete all
        keys = rdb.keys(MC_KEY_PRODUCT_DISCOUNT_PRICE.format("*"))
        for key in keys:
            rdb.delete(key)

    @classmethod
    def __flush_insert_event__(cls, target):
        super().__flush_insert_event__(target)
        target.clear_mc(target)

    @classmethod
    def __flush_after_update_event__(cls, target):
        super().__flush_after_update_event__(target)
        target.clear_mc(target)

    @classmethod
    def __flush_delete_event__(cls, target):
        super().__flush_delete_event__(target)
        target.clear_mc(target)


class SaleCategory(Model):
    __tablename__ = "discount_sale_category"
    sale_id = Column(db.Integer())
    category_id = Column(db.Integer())


class SaleProduct(Model):
    __tablename__ = "discount_sale_product"
    sale_id = Column(db.Integer())
    product_id = Column(db.Integer())
