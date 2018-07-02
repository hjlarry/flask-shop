from flaskshop.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)


class UserCart(SurrogatePK, Model):
    """A cart of a user"""

    __tablename__ = "cart_items"
    user_id = reference_col("users")
    user = relationship("User", backref="cart_items")
    product_sku_id = reference_col("product_skus")
    product_sku = relationship("ProductSku")
    amount = Column(db.Integer())

    def __repr__(self):
        return f"<Cart({self.id})>"

    def release(self, amount):
        """when submit order, release cart items in order"""
        self.amount -= amount
        if self.amount <= 0:
            self.delete()


class CouponCode(SurrogatePK, Model):
    """A promo code for an order"""

    __tablename__ = "coupon_codes"
    name = Column(db.String(255), nullable=False)
    code = Column(db.String(255), unique=True, nullable=False)
    type = Column(db.String(255), nullable=False)
    value = Column(db.String(255), nullable=False)
    total = Column(db.Integer())
    used = Column(db.Integer(), default=0)
    min_amount = Column(db.DECIMAL(10, 2))
    not_before = Column(db.DateTime())
    not_after = Column(db.DateTime())
    enabled = Column(db.Boolean(), default=True)
