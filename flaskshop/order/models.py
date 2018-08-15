from flaskshop.database import Column, Model, SurrogatePK, db, reference_col, relationship


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
