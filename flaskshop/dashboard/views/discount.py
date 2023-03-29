from flask import redirect, render_template, request, url_for, flash
from flask_babel import lazy_gettext

from flaskshop.constant import DiscountValueTypeKinds, VoucherTypeKinds
from flaskshop.dashboard.forms import SaleForm, VoucherForm
from flaskshop.dashboard.utils import wrap_partial, item_del
from flaskshop.discount.models import Sale, Voucher
from flaskshop.product.models import Category, Product


def vouchers():
    page = request.args.get("page", type=int, default=1)
    pagination = Voucher.query.paginate(page, 10)
    props = {
        "id": lazy_gettext("ID"),
        "title": lazy_gettext("Title"),
        "type_human": lazy_gettext("Type"),
        "usage_limit": lazy_gettext("Usage Limit"),
        "used": lazy_gettext("Used"),
        "discount_value_type_human": lazy_gettext("Discount Type"),
        "discount_value": lazy_gettext("Discount Value"),
    }
    context = {
        "title": lazy_gettext("Voucher"),
        "items": pagination.items,
        "props": props,
        "pagination": pagination,
        "identity": lazy_gettext("vouchers"),
    }
    return render_template("dashboard/general_list.html", **context)


def vouchers_manage(id=None):
    if id:
        voucher = Voucher.get_by_id(id)
        form = VoucherForm(obj=voucher)
    else:
        voucher = Voucher()
        form = VoucherForm()

    form.product_id.choices = [(p.id, p.title) for p in Product.query.all()]
    form.category_id.choices = [(c.id, c.title) for c in Category.query.all()]
    form.discount_value_type.choices = [
        (k.value, k.name) for k in DiscountValueTypeKinds
    ]
    form.type_.choices = [(k.value, k.name) for k in VoucherTypeKinds]

    if form.validate_on_submit():
        form.populate_obj(voucher)
        voucher.save()
        flash(lazy_gettext("Voucher saved."), "success")
        return redirect(url_for("dashboard.vouchers"))

    context = {"form": form, "title": lazy_gettext("Voucher")}
    return render_template("general_edit.html", **context)


voucher_del = wrap_partial(item_del, Voucher)


def sales():
    page = request.args.get("page", type=int, default=1)
    pagination = Sale.query.paginate(page, 10)
    props = {
        "id": lazy_gettext("ID"),
        "title": lazy_gettext("Title"),
        "discount_value_type_label": lazy_gettext("Discount Type"),
        "discount_value": lazy_gettext("Discount Value"),
    }
    context = {
        "title": lazy_gettext("Sale"),
        "items": pagination.items,
        "props": props,
        "pagination": pagination,
        "identity": lazy_gettext("sales"),
    }
    return render_template("dashboard/general_list.html", **context)


def sales_manage(id=None):
    if id:
        sale = Sale.get_by_id(id)
        form = SaleForm(obj=sale)
    else:
        sale = Sale()
        form = SaleForm()

    form.products_ids.choices = [(p.id, p.title) for p in Product.query.all()]
    form.categories_ids.choices = [(c.id, c.title) for c in Category.query.all()]
    form.discount_value_type.choices = [
        (k.value, k.name) for k in DiscountValueTypeKinds
    ]

    if form.validate_on_submit():
        tmp_p = form.products_ids.data
        tmp_c = form.categories_ids.data
        del form.products_ids
        del form.categories_ids
        form.populate_obj(sale)
        sale.save()
        sale.update_products(tmp_p)
        sale.update_categories(tmp_c)
        flash(lazy_gettext("Sale saved."), "success")
        return redirect(url_for("dashboard.sales"))

    context = {"form": form, "title": lazy_gettext("Sale")}
    return render_template("general_edit.html", **context)


sale_del = wrap_partial(item_del, Sale)
