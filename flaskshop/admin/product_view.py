import ast
from flask import url_for
from jinja2 import Markup
from flask_admin import form, actions

from flaskshop.extensions import db
from flaskshop.product.models import Product, ProductImage, ProductVariant, Category, Collection
from .utils import CustomView, CKTextAreaField


class ProductView(CustomView):
    column_list = (
        "id",
        "title",
        "first_img",
        "on_sale",
        "sold_count",
        "price",
    )
    column_sortable_list = (
        "id",
        "title",
        "sold_count",
        "price",
    )
    product_image_options = {
        "form_excluded_columns": ("created_at",),
    }
    product_variant_options = {
        "form_excluded_columns": ("created_at", "quantity_allocated"),
    }
    inline_models = [(ProductImage, product_image_options), (ProductVariant, product_variant_options)]
    column_editable_list = ('title', 'rating')
    column_filters = ('id', 'title')

    extra_js = ["//cdn.ckeditor.com/4.6.0/standard/ckeditor.js"]
    form_overrides = {"description": CKTextAreaField}

    def __init__(self):
        super().__init__(
            Product,
            db.session,
            name="Product List",
            category="product",
            endpoint="product_admin",
            menu_icon_value="nav-icon",
        )

    def _format_price(view, context, model, name):
        return Markup("￥{}".format(model.price))

    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return ''
        elif model.image.startswith('http'):
            url = model.image
        else:
            url = url_for('static', filename=form.thumbgen_filename(ast.literal_eval(model.image)[0]))
        return Markup("<img src={} width=200 height=100/>".format(url))

    column_formatters = {"price": _format_price, "image": _list_thumbnail}

    @actions.action('on_sale', 'On/Offsale')
    def action_change_on_sale(self, ids):
        try:
            query = Product.query.filter(Product.id.in_(ids))
            for p in query.all():
                p.update(on_sale=not p.on_sale)
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
        return


class ProductImageView(CustomView):
    def __init__(self):
        super().__init__(
            ProductImage,
            db.session,
            category="product",
            endpoint="product_image_admin",
            menu_icon_value="nav-icon",
        )


class ProductVariantView(CustomView):
    def __init__(self):
        super().__init__(
            ProductVariant,
            db.session,
            category="product",
            endpoint="product_variant_admin",
            menu_icon_value="nav-icon",
        )


class ProductCategoryView(CustomView):
    def __init__(self):
        super().__init__(
            Category,
            db.session,
            category="product",
            endpoint="product_category_admin",
            menu_icon_value="nav-icon",
        )


class ProductCollectionView(CustomView):
    def __init__(self):
        super().__init__(
            Collection,
            db.session,
            category="product",
            endpoint="product_collection_admin",
            menu_icon_value="nav-icon",
        )