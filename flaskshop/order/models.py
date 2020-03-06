from flask import url_for
from flask_login import current_user
from uuid import uuid4
from sqlalchemy.dialects.mysql import TINYINT

from flaskshop.database import Column, Model, db
from flaskshop.account.models import User, UserAddress
from flaskshop.product.models import ProductVariant
from flaskshop.constant import (
    OrderStatusKinds,
    PaymentStatusKinds,
    OrderEvents,
    ShipStatusKinds,
)
from flaskshop.checkout.models import ShippingMethod
from flaskshop.discount.models import Voucher


class Order(Model):
    __tablename__ = "order_order"
    token = Column(db.String(100), unique=True)
    shipping_address = Column(db.String(255))
    user_id = Column(db.Integer())
    total_net = Column(db.DECIMAL(10, 2))
    discount_amount = Column(db.DECIMAL(10, 2), default=0)
    discount_name = Column(db.String(100))
    voucher_id = Column(db.Integer())
    shipping_price_net = Column(db.DECIMAL(10, 2))
    status = Column(TINYINT())
    shipping_method_name = Column(db.String(100))
    shipping_method_id = Column(db.Integer())
    ship_status = Column(TINYINT())

    def __str__(self):
        return f"#{self.identity}"

    @classmethod
    def create_whole_order(cls, cart, note=None):
        # Step1, certify stock, voucher
        to_update_variants = []
        to_update_orderlines = []
        total_net = 0
        for line in cart.lines:
            variant = ProductVariant.get_by_id(line.variant.id)
            result, msg = variant.check_enough_stock(line.quantity)
            if result is False:
                return result, msg
            variant.quantity_allocated += line.quantity
            to_update_variants.append(variant)
            orderline = OrderLine(
                variant_id=variant.id,
                quantity=line.quantity,
                product_name=variant.display_product(),
                product_sku=variant.sku,
                product_id=variant.sku.split("-")[0],
                unit_price_net=variant.price,
                is_shipping_required=variant.is_shipping_required,
            )
            to_update_orderlines.append(orderline)
            total_net += orderline.get_total()

        voucher = None
        if cart.voucher_code:
            voucher = Voucher.get_by_code(cart.voucher_code)
            try:
                voucher.check_available(cart)
            except Exception as e:
                return False, str(e)

        # Step2, create Order obj
        try:
            shipping_method_id = None
            shipping_method_title = None
            shipping_method_price = 0
            shipping_address = None

            if cart.shipping_method_id:
                shipping_method = ShippingMethod.get_by_id(cart.shipping_method_id)
                shipping_method_id = shipping_method.id
                shipping_method_title = shipping_method.title
                shipping_method_price = shipping_method.price
                shipping_address = UserAddress.get_by_id(
                    cart.shipping_address_id
                ).full_address

            order = cls.create(
                user_id=current_user.id,
                token=str(uuid4()),
                shipping_method_id=shipping_method_id,
                shipping_method_name=shipping_method_title,
                shipping_price_net=shipping_method_price,
                shipping_address=shipping_address,
                status=OrderStatusKinds.unfulfilled.value,
                total_net=total_net,
            )
        except Exception as e:
            return False, str(e)

        # Step3, process others
        if note:
            order_note = OrderNote(
                order_id=order.id, user_id=current_user.id, content=note
            )
            db.session.add(order_note)
        if voucher:
            order.voucher_id = voucher.id
            order.discount_amount = voucher.get_vouchered_price(cart)
            order.discount_name = voucher.title
            voucher.used += 1
            db.session.add(order)
            db.session.add(voucher)
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

    @property
    def identity(self):
        return self.token.split("-")[-1]

    @property
    def total(self):
        return self.total_net + self.shipping_price_net - self.discount_amount

    @property
    def status_human(self):
        return OrderStatusKinds(int(self.status)).name

    @property
    def total_human(self):
        return "$" + str(self.total)

    @classmethod
    def get_current_user_orders(cls):
        if current_user.is_authenticated:
            orders = (
                cls.query.filter_by(user_id=current_user.id)
                .order_by(Order.id.desc())
                .all()
            )
        else:
            orders = []
        return orders

    @classmethod
    def get_user_orders(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

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
        # to resolve another instance with key is already present in this session
        local_obj = db.session.merge(self)
        db.session.add(local_obj)

        for line in self.lines:
            variant = line.variant
            variant.quantity_allocated -= line.quantity
            variant.quantity -= line.quantity
            db.session.add(variant)

        db.session.commit()

        OrderEvent.create(
            order_id=self.id,
            user_id=self.user_id,
            type_=OrderEvents.payment_captured.value,
        )

    def cancel(self):
        self.status = OrderStatusKinds.canceled.value
        db.session.add(self)

        for line in self.lines:
            variant = line.variant
            variant.quantity_allocated -= line.quantity
            db.session.add(variant)

        db.session.commit()

        OrderEvent.create(
            order_id=self.id,
            user_id=self.user_id,
            type_=OrderEvents.order_canceled.value,
        )

    def complete(self):
        self.update(status=OrderStatusKinds.completed.value)
        OrderEvent.create(
            order_id=self.id,
            user_id=self.user_id,
            type_=OrderEvents.order_completed.value,
        )

    def draft(self):
        self.update(status=OrderStatusKinds.draft.value)
        OrderEvent.create(
            order_id=self.id,
            user_id=self.user_id,
            type_=OrderEvents.draft_created.value,
        )

    def delivered(self):
        self.update(
            status=OrderStatusKinds.shipped.value,
            ship_status=ShipStatusKinds.delivered.value,
        )
        OrderEvent.create(
            order_id=self.id,
            user_id=self.user_id,
            type_=OrderEvents.order_delivered.value,
        )


class OrderLine(Model):
    __tablename__ = "order_line"
    product_name = Column(db.String(255))
    product_sku = Column(db.String(100))
    quantity = Column(db.Integer())
    unit_price_net = Column(db.DECIMAL(10, 2))
    is_shipping_required = Column(db.Boolean(), default=True)
    order_id = Column(db.Integer())
    variant_id = Column(db.Integer())
    product_id = Column(db.Integer())

    @property
    def variant(self):
        return ProductVariant.get_by_id(self.variant_id)

    def get_total(self):
        return self.unit_price_net * self.quantity


class OrderNote(Model):
    __tablename__ = "order_note"
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
    payment_no = Column(db.String(255), unique=True)
    paid_at = Column(db.DateTime())

    def pay_success(self, paid_at):
        self.paid_at = paid_at
        self.status = PaymentStatusKinds.confirmed.value
        self.save(commit=False)
        order = Order.get_by_id(self.order_id)
        order.pay_success(payment=self)

    @property
    def status_human(self):
        return PaymentStatusKinds(int(self.status)).name


class OrderEvent(Model):
    __tablename__ = "order_event"
    order_id = Column(db.Integer())
    user_id = Column(db.Integer())
    type_ = Column("type", TINYINT())
