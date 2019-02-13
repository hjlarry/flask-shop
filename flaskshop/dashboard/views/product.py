from flask import request, render_template, redirect, url_for, current_app
from flaskshop.product.models import (
    ProductAttribute,
    ProductType,
    Collection,
    Product,
    Category,
    ProductType,
)
from flaskshop.dashboard.forms import (
    AttributeForm,
    CollectionForm,
    CategoryForm,
    ProductTypeForm,
    ProductForm,
    ProductCreateForm,
)


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
        attr.update_types(form.types.data)
        attr.update_values(form.values.data)
        attr.save()
        return redirect(url_for("dashboard.attributes"))
    product_types = ProductType.query.all()
    return render_template(
        "dashboard/product/attribute.html", form=form, product_types=product_types
    )


def collections():
    page = request.args.get("page", type=int, default=1)
    pagination = Collection.query.paginate(page, 10)
    props = {"id": "ID", "title": "Title", "created_at": "Created At"}
    context = {
        "title": "Product Collection",
        "manage_endpoint": "dashboard.collection_manage",
        "items": pagination.items,
        "props": props,
        "pagination": pagination,
    }
    return render_template("dashboard/list.html", **context)


def collection_manage(id=None):
    if id:
        collection = Collection.get_by_id(id)
    else:
        collection = Collection()
    form = CollectionForm(obj=collection)
    if form.validate_on_submit():
        collection.title = form.title.data
        collection.update_products(form.products.data)
        image = form.bgimg_file.data
        background_img = image.filename
        upload_file = current_app.config["UPLOAD_DIR"] / background_img
        upload_file.write_bytes(image.read())
        collection.background_img = (
            current_app.config["UPLOAD_FOLDER"] + "/" + background_img
        )
        collection.save()
        return redirect(url_for("dashboard.collections"))
    products = Product.query.all()
    return render_template(
        "dashboard/product/collection.html", form=form, products=products
    )


def categories():
    page = request.args.get("page", type=int, default=1)
    pagination = Category.query.paginate(page, 10)
    props = {
        "id": "ID",
        "title": "Title",
        "parent": "Parent",
        "created_at": "Created At",
    }
    context = {
        "title": "Product Category",
        "manage_endpoint": "dashboard.category_manage",
        "items": pagination.items,
        "props": props,
        "pagination": pagination,
    }
    return render_template("dashboard/list.html", **context)


def category_manage(id=None):
    if id:
        category = Category.get_by_id(id)
    else:
        category = Category()
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.title = form.title.data
        category.parent_id = form.parents.data
        image = form.bgimg_file.data
        background_img = image.filename
        upload_file = current_app.config["UPLOAD_DIR"] / background_img
        upload_file.write_bytes(image.read())
        category.background_img = (
            current_app.config["UPLOAD_FOLDER"] + "/" + background_img
        )
        category.save()
        return redirect(url_for("dashboard.categories"))
    parents = Category.first_level_items()
    return render_template(
        "dashboard/product/category.html", form=form, parents=parents
    )


def product_types():
    page = request.args.get("page", type=int, default=1)
    pagination = ProductType.query.paginate(page, 10)
    props = {
        "id": "ID",
        "title": "Title",
        "has_variants": "Has Variants",
        "is_shipping_required": "Is Shipping Required",
        "created_at": "Created At",
    }
    context = {
        "title": "Product Type",
        "manage_endpoint": "dashboard.product_type_manage",
        "items": pagination.items,
        "props": props,
        "pagination": pagination,
    }
    return render_template("dashboard/list.html", **context)


def product_type_manage(id=None):
    if id:
        product_type = ProductType.get_by_id(id)
    else:
        product_type = ProductType()
    form = ProductTypeForm(obj=product_type)
    if form.validate_on_submit():
        product_type.update_product_attr(form.product_attributes.data)
        product_type.update_variant_attr(form.variant_attr_id.data)
        del form.product_attributes
        del form.variant_attr_id
        form.populate_obj(product_type)
        product_type.save()
        return redirect(url_for("dashboard.product_types"))
    attributes = ProductAttribute.query.all()
    return render_template(
        "dashboard/product/product_type.html", form=form, attributes=attributes
    )


def products():
    page = request.args.get("page", type=int, default=1)
    pagination = Product.query.paginate(page, 10)
    props = {
        "id": "ID",
        "title": "Title",
        "on_sale": "On Sale",
        "sold_count": "Sold Count",
        "price": "Price",
        "category": "Category",
    }
    context = {
        "title": "Product List",
        "items": pagination.items,
        "props": props,
        "pagination": pagination,
    }
    return render_template("dashboard/product/list.html", **context)


def product_detail(id):
    product = Product.get_by_id(id)
    return render_template("dashboard/product/detail.html", product=product)


def product_edit(id):
    product = Product.get_by_id(id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.update_images(form.images.data)
        del form.images
        form.populate_obj(product)
        product.save()
        return redirect(url_for("dashboard.product_detail", id=product.id))
    categories = Category.query.all()
    context = {"form": form, "categories": categories, "product": product}
    return render_template("dashboard/product/product_edit.html", **context)


def product_create_step1():
    form = ProductCreateForm()
    if form.validate_on_submit():
        return redirect(
            url_for(
                "dashboard.product_create_step2",
                product_type_id=form.product_type_id.data,
            )
        )
    product_types = ProductType.query.all()
    return render_template(
        "dashboard/product/product_create_step1.html",
        form=form,
        product_types=product_types,
    )


def product_create_step2():
    form = ProductForm()
    product_type_id = request.args.get("product_type_id", 1, int)
    product_type = ProductType.get_by_id(product_type_id)
    return render_template(
        "dashboard/product/product_create_step2.html",
        form=form,
        product_type=product_type,
    )

