from datetime import datetime

from flask import request, render_template, redirect, url_for

from flaskshop.discount.models import Voucher, Sale, SaleCategory, SaleProduct
from flaskshop.product.models import Product, Category
from flaskshop.dashboard.forms import VoucherForm, SaleForm
from flaskshop.constant import VoucherTypeKinds, DiscountValueTypeKinds


def vouchers():
    page = request.args.get("page", type=int, default=1)
    pagination = Voucher.query.paginate(page, 10)
    props = {
        "id": "ID",
        "title": "Title",
        "type_human": "Type",
        "usage_limit": "Usage Limit",
        "used": "Used",
        "discount_value_type_human": "Discount Type",
        "discount_value": "Discount Value",
    }
    context = {
        "title": "Voucher",
        "items": pagination.items,
        "props": props,
        "pagination": pagination,
        "identity": "vouchers",
    }
    return render_template("list.html", **context)


def vouchers_manage(id=None):
    if id:
        voucher = Voucher.get_by_id(id)
        form = VoucherForm(obj=voucher)
    else:
        form = VoucherForm()
    if form.validate_on_submit():
        if not id:
            voucher = Voucher()
        start_date, end_date = form.validity_period.data.split("-")
        voucher.start_date = datetime.strptime(start_date.strip(), "%m/%d/%Y")
        voucher.end_date = datetime.strptime(end_date.strip(), "%m/%d/%Y")
        del form.validity_period
        form.populate_obj(voucher)
        voucher.save()
        return redirect(url_for("dashboard.vouchers"))
    products = Product.query.all()
    categories = Category.query.all()
    voucher_types = [dict(id=kind.value, title=kind.name) for kind in VoucherTypeKinds]
    discount_types = [
        dict(id=kind.value, title=kind.name) for kind in DiscountValueTypeKinds
    ]
    context = {
        "form": form,
        "products": products,
        "categories": categories,
        "voucher_types": voucher_types,
        "discount_types": discount_types,
    }
    return render_template("discount/voucher.html", **context)


def sales():
    page = request.args.get("page", type=int, default=1)
    pagination = Sale.query.paginate(page, 10)
    props = {
        "id": "ID",
        "title": "Title",
        "discount_value_type_label": "Discount Type",
        "discount_value": "Discount Value",
    }
    context = {
        "title": "Sale",
        "items": pagination.items,
        "props": props,
        "pagination": pagination,
        "identity": "sales",
    }
    return render_template("list.html", **context)


def sales_manage(id=None):
    if id:
        sale = Sale.get_by_id(id)
        form = SaleForm(obj=sale)
    else:
        form = SaleForm()
    if form.validate_on_submit():
        if not id:
            sale = Sale()
        sale.update_products(form.products.data)
        sale.update_categories(form.categories.data)
        del form.products
        del form.categories
        form.populate_obj(sale)
        sale.save()
        return redirect(url_for("dashboard.sales"))
    products = Product.query.all()
    categories = Category.query.all()
    discount_types = [
        dict(id=kind.value, title=kind.name) for kind in DiscountValueTypeKinds
    ]
    context = {
        "form": form,
        "products": products,
        "categories": categories,
        "discount_types": discount_types,
    }
    return render_template("discount/sale.html", **context)
