from flask import request, render_template, redirect, url_for
from flaskshop.product.models import ProductAttribute, ProductType
from flaskshop.dashboard.forms import AttributeForm


def attributes():
    page = request.args.get("page", type=int, default=1)
    pagination = ProductAttribute.query.paginate(page, 10)
    props = {
        "id": "ID",
        "title": "Title",
        "values_label": "Value",
        "types_label": "ProductType",
    }
    context = {
        "title": "Product Attribute",
        "manage_endpoint": "dashboard.attribute_manage",
        "items": pagination.items,
        "props": props,
        "pagination": pagination,
    }
    return render_template("dashboard/list.html", **context)


def attribute_manage(id=None):
    if id:
        attr = ProductAttribute.get_by_id(id)
    else:
        attr = ProductAttribute()
    form = AttributeForm(obj=attr)
    if form.validate_on_submit():
        attr.title = form.title.data
        print(form.values.data)
        attr.update_values(form.values.data)
        attr.save()
        return redirect(url_for("dashboard.attributes"))
    product_types = ProductType.query.all()
    return render_template(
        "dashboard/product/attribute.html", form=form, product_types=product_types
    )
