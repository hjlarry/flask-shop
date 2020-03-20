import itertools
import random
import unicodedata
from uuid import uuid4

from faker import Factory
from faker.providers import BaseProvider
from sqlalchemy.sql.expression import func

from flaskshop.product.models import (
    Category,
    ProductType,
    Product,
    ProductVariant,
    ProductImage,
    ProductAttribute,
    AttributeChoiceValue,
    ProductTypeAttributes,
    ProductTypeVariantAttributes,
    Collection,
    ProductCollection,
)
from flaskshop.public.models import MenuItem, Page
from flaskshop.account.models import User, UserAddress, Role, UserRole
from flaskshop.checkout.models import ShippingMethod
from flaskshop.order.models import Order, OrderLine, OrderPayment
from flaskshop.discount.models import Voucher, Sale, SaleProduct
from flaskshop.dashboard.models import DashboardMenu
from flaskshop.settings import Config
from flaskshop.constant import (
    PaymentStatusKinds,
    DiscountValueTypeKinds,
    VoucherTypeKinds,
    OrderStatusKinds,
    Permission,
)

fake = Factory.create()


class SaleorProvider(BaseProvider):
    def money(self):
        return fake.pydecimal(2, 2, positive=True)

    def shipping_method(self):
        return random.choice(ShippingMethod.query.all())


fake.add_provider(SaleorProvider)

GROCERIES_CATEGORY = {"name": "Groceries", "image_name": "groceries.jpg"}

DEFAULT_SCHEMA = {
    "T-Shirt": {
        "category": {"name": "Apparel", "image_name": "apparel.jpg"},
        "product_attributes": {
            "Color": ["Blue", "White"],
            "Collar": ["Round", "V-Neck", "Polo"],
            "Brand": ["Saleor"],
        },
        "variant_attributes": {"Size": ["XS", "S", "M", "L", "XL", "XXL"]},
        "images_dir": "t-shirts/",
        "is_shipping_required": True,
    },
    "Mugs": {
        "category": {"name": "Accessories", "image_name": "accessories.jpg"},
        "product_attributes": {"Brand": ["Saleor"]},
        "variant_attributes": {},
        "images_dir": "mugs/",
        "is_shipping_required": True,
    },
    "Coffee": {
        "category": {
            "name": "Coffees",
            "image_name": "coffees.jpg",
            "parent": GROCERIES_CATEGORY,
        },
        "product_attributes": {
            "Coffee Genre": ["Arabica", "Robusta"],
            "Brand": ["Saleor"],
        },
        "variant_attributes": {"Box Size": ["100g", "250g", "500g", "1kg"]},
        "different_variant_prices": True,
        "images_dir": "coffee/",
        "is_shipping_required": True,
    },
    "Candy": {
        "category": {
            "name": "Candies",
            "image_name": "candies.jpg",
            "parent": GROCERIES_CATEGORY,
        },
        "product_attributes": {"Flavor": ["Sour", "Sweet"], "Brand": ["Saleor"]},
        "variant_attributes": {"Candy Box Size": ["100g", "250g", "500g"]},
        "images_dir": "candy/",
        "is_shipping_required": True,
    },
    "E-books": {
        "category": {"name": "Books", "image_name": "books.jpg"},
        "product_attributes": {
            "Author": ["John Doe", "Milionare Pirate"],
            "Publisher": ["Mirumee Press", "Saleor Publishing"],
            "Language": ["English", "Pirate"],
        },
        "variant_attributes": {},
        "images_dir": "books/",
        "is_shipping_required": False,
    },
    "Books": {
        "category": {"name": "Books", "image_name": "books.jpg"},
        "product_attributes": {
            "Author": ["John Doe", "Milionare Pirate"],
            "Publisher": ["Mirumee Press", "Saleor Publishing"],
            "Language": ["English", "Pirate"],
        },
        "variant_attributes": {"Cover": ["Soft", "Hard"]},
        "images_dir": "books/",
        "is_shipping_required": True,
    },
}
COLLECTIONS_SCHEMA = [
    {"name": "Summer collection", "image_name": "summer.jpg"},
    {"name": "Winter sale", "image_name": "sale.jpg"},
]

DASHBOARD_MENUS = [
    {"title": "CATALOG", "icon_cls": "fa-bandcamp"},
    {"title": "ORDERS", "endpoint": "orders", "icon_cls": "fa-cart-arrow-down"},
    {"title": "CUSTOMERS", "endpoint": "users", "icon_cls": "fa-user"},
    {"title": "DISCOUNTS", "icon_cls": "fa-gratipay"},
    {"title": "CONFIGURATION", "endpoint": "config_index", "icon_cls": "fa-cog"},
    {"title": "Products", "endpoint": "products", "parent_id": 1},
    {"title": "Categories", "endpoint": "categories", "parent_id": 1},
    {"title": "Collections", "endpoint": "collections", "parent_id": 1},
    {"title": "Sales", "endpoint": "sales", "parent_id": 4},
    {"title": "Vouchers", "endpoint": "vouchers", "parent_id": 4},
]

"""
Utils function
"""


def get_variant_combinations(product):
    # Returns all possible variant combinations
    # For example: product type has two variant attributes: Size, Color
    # Size has available values: [S, M], Color has values [Red, Green]
    # All combinations will be generated (S, Red), (S, Green), (M, Red),
    # (M, Green)
    # Output is list of dicts, where key is product attribute id and value is
    # attribute value id. Casted to string.
    variant_attr_map = {
        attr: attr.values for attr in product.product_type.variant_attributes
    }
    all_combinations = itertools.product(*variant_attr_map.values())
    return [
        {str(attr_value.attribute.id): str(attr_value.id) for attr_value in combination}
        for combination in all_combinations
    ]


def get_price_override(schema, combinations_num, current_price):
    prices = []
    if schema.get("different_variant_prices"):
        prices = sorted(
            [
                current_price + fake.pydecimal(2, 2, positive=True)
                for _ in range(combinations_num)
            ],
            reverse=True,
        )
    return prices


def get_name_from_attributes(variant):
    """Generates ProductVariant's name based on its attributes."""
    values = [
        attributechoice_value.title
        for attributechoice_value in variant.attribute_map.values()
    ]
    return " / ".join(values)


def get_email(first_name, last_name):
    _first = unicodedata.normalize("NFD", first_name).encode("ascii", "ignore")
    _last = unicodedata.normalize("NFD", last_name).encode("ascii", "ignore")
    return (
        f"{_first.lower().decode('utf-8')}.{_last.lower().decode('utf-8')}@example.com"
    )


"""
Fake for products data
"""

# step1
def create_products_by_schema(
    placeholder_dir, how_many, create_images, schema=DEFAULT_SCHEMA
):
    for product_type, type_schema in create_product_types_by_schema(schema):
        create_products_by_type(
            product_type,
            type_schema,
            placeholder_dir,
            how_many=how_many,
            create_images=create_images,
        )


# step2
def create_product_types_by_schema(root_schema):
    results = []
    for product_type_name, schema in root_schema.items():
        product_type = create_product_type_with_attributes(product_type_name, schema)
        results.append((product_type, schema))
    return results


# step3
def create_product_type_with_attributes(name, schema):
    product_attributes_schema = schema.get("product_attributes", {})
    variant_attributes_schema = schema.get("variant_attributes", {})
    is_shipping_required = schema.get("is_shipping_required", True)
    product_type = ProductType.get_or_create(
        title=name, is_shipping_required=is_shipping_required
    )[0]
    product_attributes = create_attributes_and_values(product_attributes_schema)
    variant_attributes = create_attributes_and_values(variant_attributes_schema)
    for attr in product_attributes:
        ProductTypeAttributes.get_or_create(
            product_type_id=product_type.id, product_attribute_id=attr.id
        )
    for attr in variant_attributes:
        ProductTypeVariantAttributes.get_or_create(
            product_type_id=product_type.id, product_attribute_id=attr.id
        )
    return product_type


# step4
def create_attributes_and_values(attribute_data):
    attributes = []
    for attribute_name, attribute_values in attribute_data.items():
        attribute, _ = ProductAttribute.get_or_create(title=attribute_name)
        for value in attribute_values:
            defaults = {"attribute_id": attribute.id, "title": value}
            AttributeChoiceValue.get_or_create(**defaults)
        attributes.append(attribute)
    return attributes


# step5
def create_products_by_type(
    product_type, schema, placeholder_dir, how_many=10, create_images=True, stdout=None
):
    category = get_or_create_category(schema["category"], placeholder_dir)

    for dummy in range(how_many):
        product = create_product(
            product_type_id=product_type.id, category_id=category.id
        )
        set_product_attributes(product, product_type)
        if create_images:
            type_placeholders = placeholder_dir / schema["images_dir"]
            create_product_images(product, random.randrange(1, 5), type_placeholders)
        variant_combinations = get_variant_combinations(product)

        prices = get_price_override(schema, len(variant_combinations), product.price)
        variants_with_prices = itertools.zip_longest(variant_combinations, prices)

        for i, variant_price in enumerate(variants_with_prices, start=1337):
            attr_combination, price = variant_price
            sku = f"{product.id}-{i}"
            create_variant(
                product, attributes=attr_combination, sku=sku, price_override=price
            )

        if not variant_combinations:
            # Create min one variant for products without variant level attrs
            sku = f"{product.id}-{fake.random_int(1000, 100000)}"
            create_variant(product, sku=sku)


# step6
def get_or_create_category(category_schema, placeholder_dir):
    if "parent" in category_schema:
        parent_id = get_or_create_category(
            category_schema["parent"], placeholder_dir
        ).id
    else:
        parent_id = 0
    category_name = category_schema["name"]
    image_name = category_schema["image_name"]
    image_dir = placeholder_dir / "products-list"
    defaults = {"background_img": str(image_dir / image_name)}
    category, _ = Category.get_or_create(
        title=category_name, parent_id=parent_id, **defaults
    )
    return category


# step7
def create_product(**kwargs):
    description = fake.paragraphs(5)
    defaults = {
        "title": fake.company(),
        "basic_price": fake.pydecimal(2, 2, positive=True),
        "description": "\n\n".join(description),
        "is_featured": random.choice([0, 1]),
    }
    defaults.update(kwargs)
    return Product.create(**defaults)


# step8
def set_product_attributes(product, product_type):
    attr_dict = {}
    for product_attribute in product_type.product_attributes:
        value = random.choice(product_attribute.values)
        attr_dict[str(product_attribute.id)] = str(value.id)

    product.attributes = attr_dict
    product.save()


# step9
def create_product_images(product, how_many, placeholder_dir):
    placeholder_root = Config.STATIC_DIR / placeholder_dir
    for dummy in range(how_many):
        image_name = random.choice(list(placeholder_root.iterdir()))
        image = str(image_name.relative_to(Config.STATIC_DIR))
        ProductImage.get_or_create(image=image, product_id=product.id)


# step10
def create_variant(product, **kwargs):
    defaults = {"product_id": product.id, "quantity": fake.random_int(1, 50)}
    defaults.update(kwargs)
    attributes = defaults.pop("attributes")
    variant = ProductVariant(**defaults)
    variant.attributes = attributes

    if variant.attributes:
        variant.title = get_name_from_attributes(variant)
    variant.save()
    return variant


# step11
def create_collections_by_schema(placeholder_dir, schema=COLLECTIONS_SCHEMA):
    for collection_data in schema:
        collection = create_fake_collection(placeholder_dir, collection_data)
        yield f"Collection: {collection}"


# step12
def create_fake_collection(placeholder_dir, collection_data):
    image_dir = placeholder_dir / "products-list"
    background_img = image_dir / collection_data["image_name"]
    collection = Collection.get_or_create(
        title=collection_data["name"], background_img=str(background_img)
    )[0]
    products = Product.query.limit(4)
    for product in products:
        ProductCollection.create(product_id=product.id, collection_id=collection.id)
    return collection


"""
Fake for account data
"""
# step13
def create_users(how_many=10):
    for dummy in range(how_many):
        user = create_fake_user()
        address = create_fake_address(user_id=user.id)
        yield f"User: {user.email}"


# step14
def create_fake_user():
    email = get_email(fake.first_name(), fake.last_name())
    user, _ = User.get_or_create(
        username=fake.first_name() + fake.last_name(),
        email=email,
        password="password",
        is_active=True,
    )
    return user


# step15
def create_fake_address(user_id=None):
    address = UserAddress.create(
        contact_name=fake.name(),
        province=fake.state(),
        city=fake.city(),
        district=fake.city_suffix(),
        address=fake.street_address(),
        contact_phone=fake.phone_number(),
        user_id=user_id,
    )
    return address


# step16
def create_roles():
    for permissions, (name, desc) in Permission.PERMISSION_MAP.items():
        Role.create(name=name, permissions=permissions)
        yield f"Role {name} created"


# step17
def create_admin():
    user = User.create(
        username="admin", email="admin@163.com", password="admin", is_active=True
    )
    create_fake_address(user.id)
    create_fake_address(user.id)
    create_fake_address(user.id)
    UserRole.create(user_id=user.id, role_id=4)
    yield f"Admin {user.username} created"
    user = User.create(username="op", email="op@163.com", password="op", is_active=True)
    UserRole.create(user_id=user.id, role_id=3)
    yield f"Admin {user.username} created"
    user = User.create(
        username="editor", email="editor@163.com", password="editor", is_active=True
    )
    UserRole.create(user_id=user.id, role_id=2)
    yield f"Admin {user.username} created"


"""
Fake for public data
"""

# step18
def create_page():
    content = """
    <h2 align="center">AN OPENSOURCE STOREFRONT PLATFORM FOR PERFECTIONISTS</h2>
    <h3 align="center">WRITTEN IN PYTHON, BEST SERVED AS A BESPOKE, HIGH-PERFORMANCE E-COMMERCE SOLUTION</h3>
    <p><br></p>
    <p><img src="http://getsaleor.com/images/main-pic.svg"></p>
    <p style="text-align: center;">
        <a href="https://github.com/mirumee/saleor/">Get Saleor</a> today!
    </p>
    """
    page_data = {
        "content": content,
        "title": "About",
        "is_visible": True,
        "slug": "about",
    }
    page, _ = Page.get_or_create(**page_data)
    yield f"Page {page.title} created"


# step19
def create_menus():
    yield "Created navbar menu"
    categories = Category.query.all()
    for category in categories:
        if not category.parent_id:
            for msg in generate_menu_items(category, menu_id=1):
                yield msg

    yield "Created footer menu"
    collection = Collection.query.first()
    item, _ = MenuItem.get_or_create(title="Collections", position=2)
    for collection in Collection.query.all():
        MenuItem.get_or_create(
            title=collection.title, collection_id=collection.id, parent_id=item.id
        )

    item, _ = MenuItem.get_or_create(title="Saleor", position=2)
    page = Page.query.first()
    if page:
        MenuItem.get_or_create(title=page.title, page_id=page.id, parent_id=item.id)
    MenuItem.get_or_create(title="Style guide", url_="/style", parent_id=item.id)


# step20
def generate_menu_items(category: Category, menu_id=None, parent_id=None):
    menu_item, created = MenuItem.get_or_create(
        title=category.title,
        category_id=category.id,
        position=menu_id,
        parent_id=parent_id,
    )

    if created:
        yield f"Created menu item for category {category}"

    for child in category.children:
        for msg in generate_menu_items(child, parent_id=menu_item.id):
            yield f"\t{msg}"


# step21
def create_shipping_methods():
    shipping_method = ShippingMethod.create(title="UPC", price=fake.money())
    yield f"Shipping method #{shipping_method.id}"
    shipping_method = ShippingMethod.create(title="DHL", price=fake.money())
    yield f"Shipping method #{shipping_method.id}"


# step22
def create_dashboard_menus():
    for item in DASHBOARD_MENUS:
        DashboardMenu.create(**item)
    yield "create dashboard menus"


"""
Fake for order data
"""
# step23
def create_orders(how_many=10):
    discounts = None
    for dummy in range(how_many):
        order = create_fake_order(discounts)
        yield f"Order: {order}"


# step24
def create_fake_order(discounts):
    user = User.query.order_by(func.random()).first()
    address = create_fake_address()
    status = random.choice(list(OrderStatusKinds)).value
    order_data = {
        "user_id": user.id,
        "shipping_address": address.full_address,
        "status": status,
        "token": str(uuid4()),
    }
    shipping_method = ShippingMethod.query.order_by(func.random()).first()
    order_data.update(
        {
            "shipping_method_name": shipping_method.title,
            "shipping_method_id": shipping_method.id,
            "shipping_price_net": shipping_method.price,
        }
    )

    order = Order.create(**order_data)
    lines = create_order_lines(order, discounts, random.randrange(1, 5))
    order.total_net = sum([line.get_total() for line in lines])
    order.save()
    create_payment(order)
    return order


# step25
def create_order_lines(order, discounts, how_many=10):
    for dummy in range(how_many):
        yield create_order_line(order, discounts)


# step26
def create_order_line(order, discounts):
    product = Product.query.order_by(func.random()).first()
    variant = product.variant[0]
    quantity = random.randrange(1, 5)
    variant.quantity += quantity
    variant.save()
    return OrderLine.create(
        order_id=order.id,
        product_name=variant.display_product(),
        product_sku=variant.sku,
        product_id=variant.sku.split("-")[0],
        is_shipping_required=variant.is_shipping_required,
        quantity=quantity,
        variant_id=variant.id,
        unit_price_net=variant.price,
    )


# step27
def create_payment(order):
    status = random.choice(list(PaymentStatusKinds)).value
    payment = OrderPayment.create(
        order_id=order.id,
        status=status,
        total=order.total_net,
        delivery=order.shipping_price_net,
        customer_ip_address=fake.ipv4(),
    )
    return payment


"""
Fake for voucher
"""

# step28
def create_product_sales(how_many=5):
    for dummy in range(how_many):
        sale = create_fake_sale()
        yield f"Sale: {sale}"


# step29
def create_fake_sale():
    sale = Sale.create(
        title=f"Happy {fake.word()} day!",
        discount_value_type=DiscountValueTypeKinds.percent.value,
        discount_value=random.choice([10, 20, 30, 40, 50]),
    )
    for product in Product.query.order_by(func.random()).all()[:4]:
        SaleProduct.create(sale_id=sale.id, product_id=product.id)
    return sale


# step30
def create_vouchers():
    defaults = {
        "type_": VoucherTypeKinds.shipping.value,
        "title": "Free shipping",
        "discount_value_type": DiscountValueTypeKinds.percent.value,
        "discount_value": 100,
    }
    voucher, created = Voucher.get_or_create(code="FREESHIPPING", **defaults)
    if created:
        yield f"Voucher #{voucher.id}"
    else:
        yield "Shipping voucher already exists"

    defaults = {
        "type_": VoucherTypeKinds.value.value,
        "title": "Big order discount",
        "discount_value_type": DiscountValueTypeKinds.fixed.value,
        "discount_value": 25,
        "limit": 200,
    }

    voucher, created = Voucher.get_or_create(code="DISCOUNT", **defaults)
    if created:
        yield f"Voucher #{voucher.id}"
    else:
        yield "Value voucher already exists"
