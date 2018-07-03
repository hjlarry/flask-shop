import json
from sqlalchemy.ext.hybrid import hybrid_property

from flaskshop.database import Column, Model, SurrogatePK, db, reference_col, relationship
from flaskshop import constant
from flask_login import current_user


class Order(SurrogatePK, Model):
    """An order of the app"""

    __tablename__ = 'orders'
    no = Column(db.String(255), nullable=False, unique=True)
    user_id = reference_col('users')
    address = Column(db.Text())
    total_amount = Column(db.DECIMAL(10, 2))
    remark = Column(db.Text())
    paid_at = Column(db.DateTime())
    coupon_code_id = reference_col('coupon_codes')
    coupon_code = relationship('CouponCode', backref='order', uselist=False)
    payment_method = Column(db.String(255))
    payment_no = Column(db.String(255), unique=True)
    refund_status = Column(db.String(255), default=constant.REFUND_STATUS_PENDING)
    refund_no = Column(db.String(255))
    closed = Column(db.Boolean(), default=False)
    reviewed = Column(db.Boolean(), default=False)
    ship_status = Column(db.String(255), default=constant.SHIP_STATUS_PENDING)
    ship_data = Column(db.Text())
    _extra = Column('extra', db.Text())

    def __repr__(self):
        return f'<Order({self.id})>'

    @hybrid_property
    def extra(self):
        if self._extra:
            return json.loads(self._extra)

    @extra.setter
    def extra(self, value):
        if isinstance(value, dict):
            self._extra = json.dumps(value)

    def can_review(self):
        if not self.paid_at:
            raise Exception('Must pay before review!')
        if self.reviewed:
            raise Exception('Has reviewed before!')
        if not self in current_user.orders:
            raise Exception('This is not your order!')
        return True

    def can_refund(self):
        if not self.paid_at:
            raise Exception('Must pay before refund!')
        if not self.refund_status == constant.REFUND_STATUS_PENDING:
            raise Exception('Has request refund before!')
        if not self in current_user.orders:
            raise Exception('This is not your order!')
        return True

    def can_recive(self):
        if not self.ship_status == constant.SHIP_STATUS_DELIVERED:
            raise Exception('Ship status is not correct!')
        if not self in current_user.orders:
            raise Exception('This is not your order!')
        return True


class OrderItem(SurrogatePK, Model):
    """Items of the order"""

    __tablename__ = 'order_items'
    order_id = reference_col('orders')
    order = relationship('Order', backref='items')
    product_id = reference_col('products')
    product = relationship('Product')
    product_sku_id = reference_col('product_skus')
    product_sku = relationship('ProductSku')
    amount = Column(db.Integer())
    rating = Column(db.Integer())
    price = Column(db.DECIMAL(10, 2))
    review = Column(db.Text())
    reviewed_at = Column(db.DateTime())

    def __repr__(self):
        return f'<OrderItem({self.id})>'
