from flask import url_for
from flask_login import current_user
from uuid import uuid4
from sqlalchemy.dialects.mysql import TINYINT

from flaskshop.database import Column, Model, db
from flaskshop.constant import OrderStatusKinds
from flaskshop.account.models import User, UserAddress
from flaskshop.product.models import ProductVariant
from flaskshop.constant import OrderStatusKinds, PaymentStatusKinds
from flaskshop.checkout.models import ShippingMethod


class Order(Model):
    __tablename__ = "order_order"
    token = Column(db.String(100), unique=True)
    shipping_address = Column(db.String(255))
    user_id = Column(db.Integer())
    total_net = Column(db.DECIMAL(10, 2))
    discount_amount = Column(db.DECIMAL(10, 2))
    discount_name = Column(db.String(100))
    voucher_id = Column(db.Integer())
    shipping_price_net = Column(db.DECIMAL(10, 2))
    status = Column(db.String(100))
    shipping_method_name = Column(db.String(100))
    shipping_method_id = Column(db.Integer())
    refund_status = Column(TINYINT())
    ship_status = Column(TINYINT())

    def __str__(self):
        return f"#{self.id}"

    @classmethod
    def create_whole_order(cls, cart, shipping_method_id, note=None):
        # Step1, process stock
        to_update_variants = []
        to_update_orderlines = []
        total = 0
        for line in cart.lines:
            variant = ProductVariant.get_by_id(line.variant.id)
            if variant.stock < line.quantity:
                return False, f"{variant.display_product()} has not enough stock"
            variant.quantity_allocated += line.quantity
            to_update_variants.append(variant)
            orderline = OrderLine(
                variant_id=variant.id,
                quantity=line.quantity,
                product_name=variant.display_product(),
                product_sku=variant.sku,
                unit_price_net=variant.price,
                is_shipping_required=variant.is_shipping_required,
            )
            to_update_orderlines.append(orderline)
            total += orderline.get_total()

        # Step2, create Order obj
        try:
            # TODO: if order not shipping required
            shipping_method = ShippingMethod.get_by_id(shipping_method_id)
            shipping_address = UserAddress.get_by_id(
                cart.shipping_address_id
            ).full_address
            total += shipping_method.price
            order = cls.create(
                user_id=current_user.id,
                token=str(uuid4()),
                shipping_method_id=shipping_method.id,
                shipping_method_name=shipping_method.title,
                shipping_price_net=shipping_method.price,
                shipping_address=shipping_address,
                status=OrderStatusKinds.unfulfilled.value,
                total_net=total,
            )
        except Exception as e:
            return False, e.msg

        # Step3, process others
        if note:
            order_note = OrderNote(
                order_id=order.id, user_id=current_user.id, content=note
            )
            db.session.add(order_note)
        for variant in to_update_variants:
            db.session.add(variant)
        for orderline in to_update_orderlines:
            orderline.order_id = order.id
            db.session.add(orderline)
        for line in cart.lines:
            db.session.delete(line)
        db.session.delete(cart)

        db.session.commit()
        return order, "success"

    def get_absolute_url(self):
        return url_for("order.show", token=self.token)

    def get_subtotal(self):
        subtotal_iterator = (line.get_total() for line in self.lines)
        return sum(subtotal_iterator)

    @property
    def identity(self):
        return self.token.split("-")[-1]

    @property
    def status_name(self):
        return OrderStatusKinds(int(self.status)).name

    @classmethod
    def get_current_user_orders(cls):
        if current_user.is_authenticated:
            orders = cls.query.filter_by(user_id=current_user.id).all()
        else:
            orders = []
        return orders

    @classmethod
    def get_user_orders(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @property
    def is_fully_paid(self):
        # TODO
        return False

    @property
    def is_pre_authorized(self):
        # TODO
        return False

    @property
    def is_open(self):
        return self.status == OrderStatusKinds.unfulfilled.value

    @property
    def is_shipping_required(self):
        return any(line.is_shipping_required for line in self.lines)

    @property
    def is_self_order(self):
        return self.user_id == current_user.id

    @property
    def lines(self):
        return OrderLine.query.filter(OrderLine.order_id == self.id).all()

    @property
    def notes(self):
        return OrderNote.query.filter(OrderNote.order_id == self.id).all()

    @property
    def user(self):
        return User.get_by_id(self.user_id)

    @property
    def payment(self):
        return OrderPayment.query.filter_by(order_id=self.id).first()

    def pay_success(self, payment):
        self.status = OrderStatusKinds.fulfilled.value
        db.session.add(self)
        db.session.add(payment)

        for line in self.lines:
            variant = line.variant
            variant.quantity_allocated -= line.quantity
            variant.quantity -= line.quantity
            db.session.add(variant)

        db.session.commit()

    def cancel_order(self):
        self.status = OrderStatusKinds.canceled.value
        db.session.add(self)

        for line in self.lines:
            variant = line.variant
            variant.quantity_allocated -= line.quantity
            db.session.add(variant)

        db.session.commit()

    def complete_order(self):
        self.update(status=OrderStatusKinds.completed.value)


class OrderLine(Model):
    __tablename__ = "order_orderline"
    product_name = Column(db.String(255))
    product_sku = Column(db.String(100))
    quantity = Column(db.Integer())
    unit_price_net = Column(db.DECIMAL(10, 2))
    is_shipping_required = Column(db.Boolean(), default=True)
    order_id = Column(db.Integer())
    variant_id = Column(db.Integer())

    @property
    def variant(self):
        return ProductVariant.get_by_id(self.variant_id)

    def get_total(self):
        return self.unit_price_net * self.quantity


class OrderNote(Model):
    __tablename__ = "order_ordernote"
    order_id = Column(db.Integer())
    user_id = Column(db.Integer())
    content = Column(db.Text())
    is_public = Column(db.Boolean(), default=True)


class OrderPayment(Model):
    __tablename__ = "order_payment"
    order_id = Column(db.Integer())
    status = Column(TINYINT)
    total = Column(db.DECIMAL(10, 2))
    delivery = Column(db.DECIMAL(10, 2))
    description = Column(db.Text())
    customer_ip_address = Column(db.String(100))
    token = Column(db.String(100))
    payment_method = Column(db.String(255))
    payment_no = Column(db.String(255), unique=True, index=True)
    paid_at = Column(db.DateTime())

    def pay_success(self, paid_at):
        self.paid_at = paid_at
        self.status = PaymentStatusKinds.confirmed.value
        order = Order.get_by_id(self.order_id)
        order.pay_success(payment=self)

