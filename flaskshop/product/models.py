from flask import url_for, request
from sqlalchemy.ext.mutable import MutableDict

from flaskshop.database import Column, Model, SurrogatePK, db


class Product(SurrogatePK, Model):
    __tablename__ = "product_product"
    __searchable__ = ["title", "description"]
    title = Column(db.String(255), nullable=False)
    description = Column(db.Text())
    on_sale = Column(db.Boolean(), default=True)
    rating = Column(db.DECIMAL(8, 2), default=5.0)
    sold_count = Column(db.Integer(), default=0)
    review_count = Column(db.Integer(), default=0)
    price = Column(db.DECIMAL(10, 2))
    category_id = Column(db.Integer())
    is_featured = Column(db.Boolean(), default=False)
    product_type_id = Column(db.Integer())
    attributes = Column(MutableDict.as_mutable(db.JSON()))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return url_for("product.show", id=self.id)

    @property
    def images(self):
        return ProductImage.query.filter(ProductImage.product_id == self.id).all()

    def get_first_img(self):
        if self.images:
            return self.images[0]
        return ""

    @property
    def first_img(self):
        return self.get_first_img()

    def __iter__(self):
        return iter(self.variants)

    @property
    def is_in_stock(self):
        return any(variant.is_in_stock for variant in self)

    @property
    def category(self):
        return Category.get_by_id(self.category_id)

    @property
    def product_type(self):
        return ProductType.get_by_id(self.product_type_id)

    @property
    def variant(self):
        return ProductVariant.query.filter(ProductVariant.product_id == self.id).all()

    @property
    def attribute_map(self):
        items = {
            ProductAttribute.get_by_id(k): AttributeChoiceValue.get_by_id(v)
            for k, v in self.attributes.items()
        }
        return items


class Category(SurrogatePK, Model):
    __tablename__ = "product_category"
    title = Column(db.String(255), nullable=False)
    parent_id = Column(db.Integer())
    background_img = Column(db.String(255))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return url_for("product.show_category", id=self.id)

    @property
    def products(self):
        all_category_ids = [child.id for child in self.children] + [self.id]
        return Product.query.filter(Product.category_id.in_(all_category_ids)).all()

    @property
    def children(self):
        return Category.query.filter(Category.parent_id == self.id).all()

    @property
    def attr_filter(self):
        attr_filter = set()
        for product in self.products:
            for attr in product.product_type.product_attributes:
                attr_filter.add(attr)
        return attr_filter

    @classmethod
    def get_product_by_category(cls, category_id, page):
        category = Category.get_by_id(category_id)
        all_category_ids = [child.id for child in category.children] + [category.id]
        query = Product.query.filter(Product.category_id.in_(all_category_ids))
        ctx, query = get_product_list_context(query, category)
        pagination = query.paginate(page, per_page=16)
        ctx.update(object=category, pagination=pagination, products=pagination.items)
        return ctx


class ProductTypeAttributes(SurrogatePK, Model):
    """存储的产品的属性是包括用户可选和不可选"""

    __tablename__ = "product_producttype_product_attributes"
    product_type_id = Column(db.Integer())
    product_attribute_id = Column(db.Integer())


class ProductTypeVariantAttributes(SurrogatePK, Model):
    """存储的产品SKU的属性是可以给用户去选择的"""

    __tablename__ = "product_producttype_variant_attributes"
    product_type_id = Column(db.Integer())
    product_attribute_id = Column(db.Integer())


class ProductType(SurrogatePK, Model):
    __tablename__ = "product_producttype"
    title = Column(db.String(255), nullable=False)
    has_variants = Column(db.Boolean(), default=True)
    is_shipping_required = Column(db.Boolean(), default=False)

    def __str__(self):
        return self.title

    @property
    def product_attributes(self):
        at_ids = (
            ProductTypeAttributes.query.with_entities(
                ProductTypeAttributes.product_attribute_id
            )
            .filter(ProductTypeAttributes.product_type_id == self.id)
            .all()
        )
        return ProductAttribute.query.filter(
            ProductAttribute.id.in_(id for id in at_ids)
        ).all()

    @property
    def variant_attributes(self):
        at_ids = (
            ProductTypeVariantAttributes.query.with_entities(
                ProductTypeVariantAttributes.product_attribute_id
            )
            .filter(ProductTypeVariantAttributes.product_type_id == self.id)
            .all()
        )
        return ProductAttribute.query.filter(
            ProductAttribute.id.in_(id for id in at_ids)
        ).all()


class ProductVariant(SurrogatePK, Model):
    __tablename__ = "product_variant"
    sku = Column(db.String(32), unique=True)
    title = Column(db.String(255))
    price_override = Column(db.DECIMAL(10, 2))
    quantity = Column(db.Integer())
    quantity_allocated = Column(db.Integer(), default=0)
    product_id = Column(db.Integer())
    attributes = Column(MutableDict.as_mutable(db.JSON()))

    def __str__(self):
        return self.title or self.sku

    def display_product(self):
        return f"{self.product} ({str(self)})"

    @property
    def is_shipping_required(self):
        return self.product.product_type.is_shipping_required

    @property
    def quantity_available(self):
        return max(self.quantity - self.quantity_allocated, 0)

    @property
    def is_in_stock(self):
        return self.quantity_available > 0

    @property
    def price(self):
        return self.price_override or self.product.price

    @property
    def product(self):
        return Product.get_by_id(self.product_id)

    def get_absolute_url(self):
        return url_for("product.show", id=self.product.id)

    @property
    def attribute_map(self):
        items = {
            ProductAttribute.get_by_id(k): AttributeChoiceValue.get_by_id(v)
            for k, v in self.attributes.items()
        }
        return items


class ProductAttribute(SurrogatePK, Model):
    __tablename__ = "product_productattribute"
    title = Column(db.String(255), nullable=False)

    def __str__(self):
        return self.title

    @property
    def values(self):
        return AttributeChoiceValue.query.filter(
            AttributeChoiceValue.attribute_id == self.id
        ).all()

    @property
    def values_label(self):
        return ",".join([value.title for value in self.values])

    @property
    def types(self):
        at_ids = (
            ProductTypeAttributes.query.with_entities(
                ProductTypeAttributes.product_type_id
            )
            .filter_by(product_attribute_id=self.id)
            .all()
        )
        return ProductType.query.filter(ProductType.id.in_(id for id in at_ids)).all()

    @property
    def types_label(self):
        return ",".join([t.title for t in self.types])

    def update_values(self, new_values):
        origin_values = list(value.title for value in self.values)
        need_del = set()
        need_add = set()
        for value in self.values:
            if value.title not in new_values:
                need_del.add(value)
        for value in new_values:
            if value not in origin_values:
                need_add.add(value)
        for value in need_del:
            value.delete()
        for value in need_add:
            AttributeChoiceValue.create(title=value, attribute_id=self.id)

    def update_types(self, new_types):
        origin_ids = (
            ProductTypeAttributes.query.with_entities(
                ProductTypeAttributes.product_type_id
            )
            .filter_by(product_attribute_id=self.id)
            .all()
        )
        origin_ids = set(i for i, in origin_ids)
        new_types = set(int(i) for i in new_types)
        need_del = origin_ids - new_types
        need_add = new_types - origin_ids
        for id in need_del:
            ProductTypeAttributes.query.filter_by(
                product_attribute_id=self.id, product_type_id=id
            ).first().delete()
        for id in need_add:
            ProductTypeAttributes.create(
                product_attribute_id=self.id, product_type_id=id
            )


class AttributeChoiceValue(SurrogatePK, Model):
    __tablename__ = "product_attributechoicevalue"
    title = Column(db.String(255), nullable=False)
    attribute_id = Column(db.Integer())

    def __str__(self):
        return self.title

    @property
    def attribute(self):
        return ProductAttribute.get_by_id(self.attribute_id)


class ProductImage(SurrogatePK, Model):
    __tablename__ = "product_productimage"
    image = Column(db.String(255))
    order = Column(db.Integer())
    product_id = Column(db.Integer())

    def __str__(self):
        return url_for("static", filename=self.image, _external=True)


class Collection(SurrogatePK, Model):
    __tablename__ = "product_collection"
    title = Column(db.String(255), nullable=False)
    background_img = Column(db.String(255))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return url_for("product.show_collection", id=self.id)

    @property
    def products(self):
        at_ids = (
            ProductCollection.query.with_entities(ProductCollection.product_id)
            .filter(ProductCollection.collection_id == self.id)
            .all()
        )
        return Product.query.filter(Product.id.in_(id for id in at_ids)).all()

    @property
    def attr_filter(self):
        # TODO cache
        attr_filter = set()
        for product in self.products:
            for attr in product.product_type.product_attributes:
                attr_filter.add(attr)
        return attr_filter

    def update_products(self, new_products):
        origin_ids = (
            ProductCollection.query.with_entities(ProductCollection.product_id)
            .filter_by(collection_id=self.id)
            .all()
        )
        origin_ids = set(i for i, in origin_ids)
        new_products = set(int(i) for i in new_products)
        need_del = origin_ids - new_products
        need_add = new_products - origin_ids
        for id in need_del:
            ProductCollection.query.filter_by(
                collection_id=self.id, product_id=id
            ).first().delete()
        for id in need_add:
            ProductCollection.create(collection_id=self.id, product_id=id)


class ProductCollection(SurrogatePK, Model):
    __tablename__ = "product_collection_products"
    product_id = Column(db.Integer())
    collection_id = Column(db.Integer())

    @classmethod
    def get_product_by_collection(cls, collection_id, page):
        collection = Collection.get_by_id(collection_id)
        at_ids = (
            ProductCollection.query.with_entities(ProductCollection.product_id)
            .filter(ProductCollection.collection_id == collection.id)
            .all()
        )
        query = Product.query.filter(Product.id.in_(id for id in at_ids))
        ctx, query = get_product_list_context(query, collection)
        pagination = query.paginate(page, per_page=16)
        ctx.update(object=collection, pagination=pagination, products=pagination.items)
        return ctx


def get_product_list_context(query, obj):
    """
    obj: collection or category, to get it`s attr_filter.
    """
    args_dict = {}

    price_from = request.args.get("price_from", None, type=int)
    price_to = request.args.get("price_to", None, type=int)
    if price_from:
        query = query.filter(Product.price > price_from)
    if price_to:
        query = query.filter(Product.price < price_to)
    args_dict.update(price_from=price_from, price_to=price_to)

    sort_by_choices = {"title": "title", "price": "price"}
    arg_sort_by = request.args.get("sort_by", "")
    is_descending = False
    if arg_sort_by.startswith("-"):
        is_descending = True
        arg_sort_by = arg_sort_by[1:]
    if arg_sort_by in sort_by_choices:
        query = (
            query.order_by(desc(getattr(Product, arg_sort_by)))
            if is_descending
            else query.order_by(getattr(Product, arg_sort_by))
        )
    now_sorted_by = arg_sort_by or "title"
    args_dict.update(
        sort_by_choices=sort_by_choices,
        now_sorted_by=now_sorted_by,
        is_descending=is_descending,
    )

    args_dict.update(default_attr={})
    attr_filter = obj.attr_filter
    for attr in attr_filter:
        value = request.args.get(attr.title)
        if value:
            query = query.filter(Product.attributes.__getitem__(str(attr.id)) == value)
            args_dict["default_attr"].update({attr.title: int(value)})
    args_dict.update(attr_filter=attr_filter)

    if request.args:
        args_dict.update(clear_filter=True)

    return args_dict, query
