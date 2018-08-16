from flask import url_for

from flaskshop.database import Column, Model, SurrogatePK, db, reference_col, relationship
from flaskshop.constant import ORDER_STATUS_UNFULFILLED, ORDER_STATUS_PARTIALLY_FULFILLED


class Order(SurrogatePK, Model):
    __tablename__ = 'order_order'
    token = Column(db.String(100))
    shipping_address_id = reference_col('users_address')
    shipping_address = relationship('UserAddress')
    user_id = reference_col('users')
    total_net = Column(db.DECIMAL(10, 2))
    discount_amount = Column(db.DECIMAL(10, 2))
    discount_name = Column(db.String(100))
    voucher_id = reference_col('discount_voucher')
    shipping_price_net = Column(db.DECIMAL(10, 2))
    status = Column(db.String(100))
    shipping_method_name = Column(db.String(100))
    shipping_method_id = reference_col('checkout_shippingmethod')

    def __str__(self):
        return f"#{self.id}"

    def get_absolute_url(self):
        return url_for('order.show', id=self.id)

    def is_fully_paid(self):
        # TODO
        return False

    def is_pre_authorized(self):
        # TODO
        return False

    def is_open(self):
        statuses = {ORDER_STATUS_UNFULFILLED, ORDER_STATUS_PARTIALLY_FULFILLED}
        return self.status in statuses

    def is_shipping_required(self):
        return any(line.is_shipping_required for line in self.lines)

    def get_subtotal(self):
        subtotal_iterator = (line.get_total() for line in self.lines)
        return sum(subtotal_iterator)


class OrderLine(SurrogatePK, Model):
    __tablename__ = 'order_orderline'
    product_name = Column(db.String(255))
    product_sku = Column(db.String(100))
    quantity = Column(db.Integer())
    unit_price_net = Column(db.DECIMAL(10, 2))
    is_shipping_required = Column(db.Boolean(), default=True)
    order_id = reference_col('order_order')
    order = relationship('Order', backref='lines')
    variant_id = reference_col('product_variant')
    variant = relationship('ProductVariant')

    def get_total(self):
        return self.unit_price_net * self.quantity


class OrderNote(SurrogatePK, Model):
    __tablename__ = 'order_ordernote'
    order_id = reference_col('order_order')
    order = relationship('Order', backref='notes')
    user_id = reference_col('users')
    content = Column(db.Text())
    is_public = Column(db.Boolean(), default=True)


class OrderPayment(SurrogatePK, Model):
    __tablename__ = 'order_payment'
    order_id = reference_col('order_order')
    order = relationship('Order', backref=db.backref("payment", uselist=False))
    status = Column(db.String(100))
    total = Column(db.DECIMAL(10, 2))
    delivery = Column(db.DECIMAL(10, 2))
    description = Column(db.Text())
    customer_ip_address = Column(db.String(100))
    token = Column(db.String(100))
    payment_method = Column(db.String(255))
    payment_no = Column(db.String(255), unique=True)
