from wtforms.fields import SelectField
from jinja2 import Markup

from flaskshop.order.models import Order, OrderLine
from flaskshop.constant import *
from flaskshop.extensions import db
from .utils import CustomView


class OrderView(CustomView):
    can_create = False
    column_list = ("id", "no", "user", "total_net", "status")
    inline_models = (OrderLine,)
    form_excluded_columns = ("user",)
    form_extra_fields = {
        "refund_status": SelectField(
            choices=[
                (REFUND_STATUS_APPLIED, REFUND_STATUS_APPLIED),
                (REFUND_STATUS_FAILED, REFUND_STATUS_FAILED),
                (REFUND_STATUS_PENDING, REFUND_STATUS_PENDING),
                (REFUND_STATUS_PROCESSING, REFUND_STATUS_PROCESSING),
                (REFUND_STATUS_SUCCESS, REFUND_STATUS_SUCCESS),
            ]
        ),
        "ship_status": SelectField(
            choices=[
                (SHIP_STATUS_DELIVERED, SHIP_STATUS_DELIVERED),
                (SHIP_STATUS_PENDING, SHIP_STATUS_PENDING),
                (SHIP_STATUS_RECEIVED, SHIP_STATUS_RECEIVED),
            ]
        ),
    }

    def __init__(self):
        super().__init__(
            Order,
            db.session,
            endpoint="order_admin",
            menu_icon_value="fa-cart-arrow-down nav-icon",
        )

    def _format_price(view, context, model, name):
        return Markup("￥{}".format(model.total_amount))

    column_formatters = {"total_amount": _format_price}
