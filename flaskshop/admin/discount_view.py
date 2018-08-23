from flaskshop.discount.models import Sale, Voucher
from flaskshop.extensions import db
from .utils import CustomView


class SaleView(CustomView):
    def __init__(self):
        super().__init__(
            Sale,
            db.session,
            category="promotion",
            endpoint="sale_admin",
            menu_icon_value="nav-icon",
        )


class VoucherView(CustomView):
    def __init__(self):
        super().__init__(
            Voucher,
            db.session,
            category="promotion",
            endpoint="voucher_admin",
            menu_icon_value="nav-icon",
        )
