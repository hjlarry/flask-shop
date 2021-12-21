import itertools

from flask import url_for, request, current_app
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import desc

from flaskshop.database import Column, Model, db
from flaskshop.corelib.mc import cache, cache_by_args, rdb
from flaskshop.corelib.db import PropsItem
from flaskshop.settings import Config


MC_KEY_FEATURED_PRODUCTS = "product:featured:{}"
MC_KEY_PRODUCT_IMAGES = "product:product:{}:images"
MC_KEY_PRODUCT_VARIANT = "product:product:{}:variant"
MC_KEY_PRODUCT_DISCOUNT_PRICE = "product:product:{}:discount_price"
MC_KEY_ATTRIBUTE_VALUES = "product:attribute:values:{}"
MC_KEY_COLLECTION_PRODUCTS = "product:collection:{}:products:{}"
MC_KEY_CATEGORY_PRODUCTS = "product:category:{}:products:{}"
MC_KEY_CATEGORY_CHILDREN = "product:category:{}:children"


class Product(Model):
    __tablename__ = "product_product"
    title = Column(db.String(255), nullable=False)
    on_sale = Column(db.Boolean(), default=True)
    rating = Column(db.DECIMAL(8, 2), default=5.0)
    sold_count = Column(db.Integer(), default=0)
    review_count = Column(db.Integer(), default=0)
    basic_price = Column(db.DECIMAL(10, 2))
    category_id = Column(db.Integer())
    is_featured = Column(db.Boolean(), default=False)
    product_type_id = Column(db.Integer())
    attributes = Column(MutableDict.as_mutable(db.JSON()))
    description = Column(db.Text())
    if Config.USE_REDIS:
        description = PropsItem("description")

    def __str__(self):
        return self.title

    def __iter__(self):
        return iter(self.variants)

    def get_absolute_url(self):
        return url_for("product.show", id=self.id)

    @property
    @cache(MC_KEY_PRODUCT_IMAGES.format("{self.id}"))
    def images(self):
        return ProductImage.query.filter(ProductImage.product_id == self.id).all()

    @property
    def first_img(self):
        if self.images:
            return str(self.images[0])
        return ""

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
    def is_discounted(self):
        if float(self.discounted_price) > 0:
            return True
        return False

    @property
    @cache(MC_KEY_PRODUCT_DISCOUNT_PRICE.format("{self.id}"))
    def discounted_price(self):
        from flaskshop.discount.models import Sale

        return Sale.get_discounted_price(self)

    @property
    def price(self):
        if self.is_discounted:
            return self.basic_price - self.discounted_price
        return self.basic_price

    @property
    def price_human(self):
        return "$" + str(self.price)

    @property
    def on_sale_human(self):
        return "Y" if self.on_sale else "N"

    @property
    @cache(MC_KEY_PRODUCT_VARIANT.format("{self.id}"))
    def variant(self):
        return ProductVariant.query.filter(ProductVariant.product_id == self.id).all()

    @property
    def attribute_map(self):
        items = {
            ProductAttribute.get_by_id(k): AttributeChoiceValue.get_by_id(v)
            for k, v in self.attributes.items()
        }
        return items

    @classmethod
    @cache(MC_KEY_FEATURED_PRODUCTS.format("{num}"))
    def get_featured_product(cls, num=8):
        return cls.query.filter_by(is_featured=True).limit(num).all()

    def update_images(self, new_images):
        origin_ids = (
            ProductImage.query.with_entities(ProductImage.product_id)
            .filter_by(product_id=self.id)
            .all()
        )
        origin_ids = set(i for i, in origin_ids)
        new_images = set(int(i) for i in new_images)
        need_del = origin_ids - new_images
        need_add = new_images - origin_ids
        for id in need_del:
            ProductImage.get_by_id(id).delete(commit=False)
        for id in need_add:
            image = ProductImage.get_by_id(id)
            image.product_id = self.id
            image.save(commit=False)
        db.session.commit()

    def update_attributes(self, attr_values):
        attr_entries = [str(item.id) for item in self.product_type.product_attributes]
        attributes = dict(zip(attr_entries, attr_values))
        self.attributes = attributes

    def generate_variants(self):
        if not self.product_type.has_variants:
            ProductVariant.create(sku=str(self.id) + "-1337", product_id=self.id)
        else:
            sku_id = 1337
            variant_attributes = self.product_type.variant_attributes[0]
            for value in variant_attributes.values:
                sku = str(self.id) + "-" + str(sku_id)
                attributes = {str(variant_attributes.id): str(value.id)}
                ProductVariant.create(
                    sku=sku,
                    title=value.title,
                    product_id=self.id,
                    attributes=attributes,
                )
                sku_id += 1

    def delete(self):
        need_del_collection_products = ProductCollection.query.filter_by(
            product_id=self.id
        ).all()
        for item in itertools.chain(
            self.images, self.variant, need_del_collection_products
        ):
            item.delete(commit=False)
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def clear_mc(target):
        rdb.delete(MC_KEY_PRODUCT_DISCOUNT_PRICE.format(target.id))
        keys = rdb.keys(MC_KEY_FEATURED_PRODUCTS.format("*"))
        for key in keys:
            rdb.delete(key)

    @staticmethod
    def clear_category_cache(target):
        keys = rdb.keys(MC_KEY_CATEGORY_PRODUCTS.format(target.category_id, "*"))
        for key in keys:
            rdb.delete(key)

    @classmethod
    def __flush_insert_event__(cls, target):
        super().__flush_insert_event__(target)

        if current_app.config["USE_ES"]:
            from flaskshop.public.search import Item

            Item.add(target)

    @classmethod
    def __flush_before_update_event__(cls, target):

        super().__flush_before_update_event__(target)
        target.clear_category_cache(target)

    @classmethod
    def __flush_after_update_event__(cls, target):

        super().__flush_after_update_event__(target)
        target.clear_mc(target)
        target.clear_category_cache(target)
        if current_app.config["USE_ES"]:
            from flaskshop.public.search import Item

            Item.update_item(target)

    @classmethod
    def __flush_delete_event__(cls, target):
        from flaskshop.public.search import Item

        super().__flush_delete_event__(target)
        target.clear_mc(target)
        target.clear_category_cache(target)
        Item.delete(target)


class Category(Model):
    __tablename__ = "product_category"
    title = Column(db.String(255), nullable=False)
    parent_id = Column(db.Integer(), default=0)
    background_img = Column(db.String(255))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return url_for("product.show_category", id=self.id)

    @property
    def background_img_url(self):
        return url_for("static", filename=self.background_img)

    @property
    def products(self):
        all_category_ids = [child.id for child in self.children] + [self.id]
        return Product.query.filter(Product.category_id.in_(all_category_ids)).all()

    @property
    @cache(MC_KEY_CATEGORY_CHILDREN.format("{self.id}"))
    def children(self):
        return Category.query.filter(Category.parent_id == self.id).all()

    @property
    def parent(self):
        return Category.get_by_id(self.parent_id)

    @property
    def attr_filter(self):
        attr_filter = set()
        for product in self.products:
            for attr in product.product_type.product_attributes:
                attr_filter.add(attr)
        return attr_filter

    @classmethod
    @cache_by_args(MC_KEY_CATEGORY_PRODUCTS.format("{category_id}", "{page}"))
    def get_product_by_category(cls, category_id, page):
        category = Category.get_by_id(category_id)
        all_category_ids = [child.id for child in category.children] + [category.id]
        query = Product.query.filter(Product.category_id.in_(all_category_ids))
        ctx, query = get_product_list_context(query, category)
        pagination = query.paginate(page, per_page=16)
        del pagination.query
        ctx.update(object=category, pagination=pagination, products=pagination.items)
        return ctx

    @classmethod
    def first_level_items(cls):
        return cls.query.filter(cls.parent_id == 0).all()

    def delete(self):
        for child in self.children:
            child.parent_id = 0
            db.session.add(child)
        need_update_products = Product.query.filter_by(category_id=self.id).all()
        for product in need_update_products:
            product.category_id = 0
            db.session.add(product)
        db.session.delete(self)
        db.session.commit()
        if self.background_img:
            image = current_app.config["STATIC_DIR"] / self.background_img
            if image.exists():
                image.unlink()

    @staticmethod
    def clear_mc(target):
        rdb.delete(MC_KEY_CATEGORY_CHILDREN.format(target.id))
        keys = rdb.keys(MC_KEY_CATEGORY_PRODUCTS.format(target.id, "*"))
        for key in keys:
            rdb.delete(key)

    @classmethod
    def __flush_after_update_event__(cls, target):
        super().__flush_after_update_event__(target)
        target.clear_mc(target)

    @classmethod
    def __flush_delete_event__(cls, target):
        super().__flush_delete_event__(target)
        target.clear_mc(target)


class ProductTypeAttributes(Model):
    """存储的产品的属性是包括用户可选和不可选"""

    __tablename__ = "product_type_attribute"
    product_type_id = Column(db.Integer())
    product_attribute_id = Column(db.Integer())


class ProductTypeVariantAttributes(Model):
    """存储的产品SKU的属性是可以给用户去选择的"""

    __tablename__ = "product_type_variant_attribute"
    product_type_id = Column(db.Integer())
    product_attribute_id = Column(db.Integer())


class ProductType(Model):
    __tablename__ = "product_type"
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
            ProductAttribute.id.in_(id for id, in at_ids)
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
            ProductAttribute.id.in_(id for id, in at_ids)
        ).all()

    @property
    def variant_attr_id(self):
        if self.variant_attributes:
            return self.variant_attributes[0].id
        else:
            return None

    def update_product_attr(self, new_attrs):
        origin_ids = (
            ProductTypeAttributes.query.with_entities(
                ProductTypeAttributes.product_attribute_id
            )
            .filter_by(product_type_id=self.id)
            .all()
        )
        origin_ids = set(i for i, in origin_ids)
        new_attrs = set(int(i) for i in new_attrs)
        need_del = origin_ids - new_attrs
        need_add = new_attrs - origin_ids
        for id in need_del:
            ProductTypeAttributes.query.filter_by(
                product_type_id=self.id, product_attribute_id=id
            ).first().delete(commit=False)
        for id in need_add:
            new = ProductTypeAttributes(
                product_type_id=self.id, product_attribute_id=id
            )
            db.session.add(new)
        db.session.commit()

    def update_variant_attr(self, variant_attr):
        origin_attr = ProductTypeVariantAttributes.query.filter_by(
            product_type_id=self.id
        ).first()
        if origin_attr:
            origin_attr.product_attribute_id = variant_attr
            origin_attr.save()
        else:
            ProductTypeVariantAttributes.create(
                product_type_id=self.id, product_attribute_id=variant_attr
            )

    def delete(self):
        need_del_product_attrs = ProductTypeAttributes.query.filter_by(
            product_type_id=self.id
        ).all()
        need_del_variant_attrs = ProductTypeVariantAttributes.query.filter_by(
            product_type_id=self.id
        ).all()

        for item in itertools.chain(need_del_product_attrs, need_del_variant_attrs):
            item.delete(commit=False)
        need_update_products = Product.query.filter_by(product_type_id=self.id).all()
        for product in need_update_products:
            product.product_type_id = 0
            db.session.add(product)
        db.session.delete(self)
        db.session.commit()


class ProductVariant(Model):
    __tablename__ = "product_variant"
    sku = Column(db.String(32), unique=True)
    title = Column(db.String(255))
    price_override = Column(db.DECIMAL(10, 2), default=0.00)
    quantity = Column(db.Integer(), default=0)
    quantity_allocated = Column(db.Integer(), default=0)
    product_id = Column(db.Integer(), default=0)
    attributes = Column(MutableDict.as_mutable(db.JSON()))

    def __str__(self):
        return self.title or self.sku

    def display_product(self):
        return f"{self.product} ({str(self)})"

    @property
    def sku_id(self):
        return self.sku.split("-")[1]

    @sku_id.setter
    def sku_id(self, data):
        pass

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
    def stock(self):
        return self.quantity - self.quantity_allocated

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

    def check_enough_stock(self, quantity):
        if self.stock < quantity:
            return False, f"{self.display_product()} has not enough stock"
        return True, "success"

    @staticmethod
    def clear_mc(target):
        rdb.delete(MC_KEY_PRODUCT_VARIANT.format(target.product_id))

    @classmethod
    def __flush_insert_event__(cls, target):
        super().__flush_insert_event__(target)
        target.clear_mc(target)

    @classmethod
    def __flush_after_update_event__(cls, target):
        super().__flush_after_update_event__(target)
        target.clear_mc(target)

    @classmethod
    def __flush_delete_event__(cls, target):
        super().__flush_delete_event__(target)
        target.clear_mc(target)


class ProductAttribute(Model):
    __tablename__ = "product_attribute"
    title = Column(db.String(255), nullable=False)

    def __str__(self):
        return self.title

    @property
    @cache(MC_KEY_ATTRIBUTE_VALUES.format("{self.id}"))
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
        return ProductType.query.filter(ProductType.id.in_(id for id, in at_ids)).all()

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
            value.delete(commit=False)
        for value in need_add:
            new = AttributeChoiceValue(title=value, attribute_id=self.id)
            db.session.add(new)
        db.session.commit()

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
            ).first().delete(commit=False)
        for id in need_add:
            new = ProductTypeAttributes(
                product_attribute_id=self.id, product_type_id=id
            )
            db.session.add(new)
        db.session.commit()

    def delete(self):
        need_del_product_attrs = ProductTypeAttributes.query.filter_by(
            product_attribute_id=self.id
        ).all()
        need_del_variant_attrs = ProductTypeVariantAttributes.query.filter_by(
            product_attribute_id=self.id
        ).all()
        for item in itertools.chain(
            need_del_product_attrs, need_del_variant_attrs, self.values
        ):
            item.delete(commit=False)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def __flush_after_update_event__(cls, target):
        super().__flush_after_update_event__(target)
        rdb.delete(MC_KEY_ATTRIBUTE_VALUES.format(target.id))

    @classmethod
    def __flush_delete_event__(cls, target):
        super().__flush_delete_event__(target)
        rdb.delete(MC_KEY_ATTRIBUTE_VALUES.format(target.id))


class AttributeChoiceValue(Model):
    __tablename__ = "product_attribute_value"
    title = Column(db.String(255), nullable=False)
    attribute_id = Column(db.Integer())

    def __str__(self):
        return self.title

    @property
    def attribute(self):
        return ProductAttribute.get_by_id(self.attribute_id)


class ProductImage(Model):
    __tablename__ = "product_image"
    image = Column(db.String(255))
    order = Column(db.Integer())
    product_id = Column(db.Integer())

    def __str__(self):
        return url_for("static", filename=self.image, _external=True)

    @staticmethod
    def clear_mc(target):
        rdb.delete(MC_KEY_PRODUCT_IMAGES.format(target.product_id))

    @classmethod
    def __flush_insert_event__(cls, target):
        super().__flush_insert_event__(target)
        target.clear_mc(target)

    @classmethod
    def __flush_delete_event__(cls, target):
        super().__flush_delete_event__(target)
        target.clear_mc(target)
        image_file = current_app.config["STATIC_DIR"] / target.image
        if image_file.exists():
            image_file.unlink()


class Collection(Model):
    __tablename__ = "product_collection"
    title = Column(db.String(255), nullable=False)
    background_img = Column(db.String(255))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return url_for("product.show_collection", id=self.id)

    @property
    def background_img_url(self):
        return url_for("static", filename=self.background_img)

    @property
    def products(self):
        at_ids = (
            ProductCollection.query.with_entities(ProductCollection.product_id)
            .filter_by(collection_id=self.id)
            .all()
        )
        return Product.query.filter(Product.id.in_(id for id, in at_ids)).all()

    @property
    def attr_filter(self):
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
            ).first().delete(commit=False)
        for id in need_add:
            new = ProductCollection(collection_id=self.id, product_id=id)
            db.session.add(new)
        db.session.commit()

    def delete(self):
        need_del = ProductCollection.query.filter_by(collection_id=self.id).all()
        for item in need_del:
            item.delete(commit=False)
        db.session.delete(self)
        db.session.commit()
        if self.background_img:
            image = current_app.config["STATIC_DIR"] / self.background_img
            if image.exists():
                image.unlink()


class ProductCollection(Model):
    __tablename__ = "product_collection_product"
    product_id = Column(db.Integer())
    collection_id = Column(db.Integer())

    @classmethod
    @cache_by_args(MC_KEY_COLLECTION_PRODUCTS.format("{collection_id}", "{page}"))
    def get_product_by_collection(cls, collection_id, page):
        collection = Collection.get_by_id(collection_id)
        at_ids = (
            ProductCollection.query.with_entities(ProductCollection.product_id)
            .filter(ProductCollection.collection_id == collection.id)
            .all()
        )
        query = Product.query.filter(Product.id.in_(id for id, in at_ids))
        ctx, query = get_product_list_context(query, collection)
        pagination = query.paginate(page, per_page=16)
        del pagination.query
        ctx.update(object=collection, pagination=pagination, products=pagination.items)
        return ctx

    @staticmethod
    def clear_mc(target):
        keys = rdb.keys(MC_KEY_COLLECTION_PRODUCTS.format(target.collection_id, "*"))
        for key in keys:
            rdb.delete(key)

    @classmethod
    def __flush_insert_event__(cls, target):
        target.clear_mc(target)

    @classmethod
    def __flush_after_update_event__(cls, target):
        super().__flush_after_update_event__(target)
        target.clear_mc(target)

    @classmethod
    def __flush_delete_event__(cls, target):
        super().__flush_delete_event__(target)
        target.clear_mc(target)


def get_product_list_context(query, obj):
    """
    obj: collection or category, to get it`s attr_filter.
    """
    args_dict = {}
    price_from = request.args.get("price_from", None, type=int)
    price_to = request.args.get("price_to", None, type=int)
    if price_from:
        query = query.filter(Product.basic_price > price_from)
    if price_to:
        query = query.filter(Product.basic_price < price_to)
    args_dict.update(price_from=price_from, price_to=price_to)

    sort_by_choices = {"title": "title", "price": "price"}
    arg_sort_by = request.args.get("sort_by", "")
    is_descending = False
    if arg_sort_by.startswith("-"):
        is_descending = True
        arg_sort_by = arg_sort_by[1:]
    if arg_sort_by in sort_by_choices:
        if is_descending:
            query = query.order_by(desc(getattr(Product, arg_sort_by)))
        else:
            query = query.order_by(getattr(Product, arg_sort_by))
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
