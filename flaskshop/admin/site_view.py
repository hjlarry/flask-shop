from flaskshop.public.models import Site, MenuItem, Page
from flaskshop.product.models import ProductType, ProductAttribute
from flaskshop.extensions import db
from .utils import CustomView


class SiteView(CustomView):
    def __init__(self):
        super().__init__(
            Site,
            db.session,
            category="config",
            endpoint="site_admin",
            menu_icon_value="nav-icon",
        )


class MenuItemView(CustomView):
    def __init__(self):
        super().__init__(
            MenuItem,
            db.session,
            category="config",
            endpoint="menu_item_admin",
            menu_icon_value="nav-icon",
        )


class PageView(CustomView):
    def __init__(self):
        super().__init__(
            Page,
            db.session,
            category="config",
            endpoint="page_admin",
            menu_icon_value="nav-icon",
        )


class ProductTypeView(CustomView):
    def __init__(self):
        super().__init__(
            ProductType,
            db.session,
            category="config",
            endpoint="product_type_admin",
            menu_icon_value="nav-icon",
        )


class ProductAttributeView(CustomView):
    def __init__(self):
        super().__init__(
            ProductAttribute,
            db.session,
            category="config",
            endpoint="product_attribute_admin",
            menu_icon_value="nav-icon",
        )
