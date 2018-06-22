from flaskshop.database import Column, Model, SurrogatePK, db, reference_col, relationship
from flaskshop import utils


class Order(SurrogatePK, Model):
    """An order of the app"""

    __tablename__ = 'orders'
    no = Column(db.String(255), nullable=False, unique=True)
    user_id = Column(db.Integer())
    address = Column(db.Text())
    total_amount = Column(db.DECIMAL(10, 2))
    remark = Column(db.Text())
    paid_at = Column(db.DateTime())
    payment_method = Column(db.String(255))
    payment_no = Column(db.String(255))
    refund_status = Column(db.String(255), default=utils.REFUND_STATUS_PENDING)
    refund_no = Column(db.String(255))
    closed = Column(db.Boolean(), default=False)
    reviewed = Column(db.Boolean(), default=False)
    ship_status = Column(db.String(255), default=utils.SHIP_STATUS_PENDING)
    ship_data = Column(db.Text())
    extra = Column(db.Text())


class OrderItem(SurrogatePK, Model):
    """An order of the app"""

    __tablename__ = 'order_items'
    order_id = Column(db.Integer())
    product_id = Column(db.Integer())
    product_sku_id = Column(db.Integer())
    amount = Column(db.Integer())
    rating = Column(db.Integer())
    price = Column(db.DECIMAL(10, 2))
    review = Column(db.Text())
    reviewed_at = Column(db.DateTime())
