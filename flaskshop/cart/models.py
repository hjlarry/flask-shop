from flaskshop.database import Column, Model, SurrogatePK, db, reference_col, relationship


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
