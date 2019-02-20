import itertools
import random
import unicodedata
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
    ProductCollection
)
from flaskshop.public.models import Site, MenuItem, Page
from flaskshop.account.models import User, UserAddress
from flaskshop.checkout.models import ShippingMethod
from flaskshop.order.models import Order, OrderLine, OrderPayment
from flaskshop.discount.models import Voucher, Sale, SaleProduct
from flaskshop.dashboard.models import DashboardMenu
from flaskshop.settings import Config
from flaskshop.constant import (
    PAYMENT_STATUS_WAITING,
    PAYMENT_STATUS_PREAUTH,
    PAYMENT_STATUS_CONFIRMED,
    TYPE_PERCENT,
    TYPE_FIXED,
    VOUCHER_TYPE_SHIPPING,
    VOUCHER_TYPE_VALUE,
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


def create_attributes_and_values(attribute_data):
    attributes = []
    for attribute_name, attribute_values in attribute_data.items():
        attribute, _ = ProductAttribute.get_or_create(title=attribute_name)
        for value in attribute_values:
            defaults = {"attribute_id": attribute.id, "title": value}
            AttributeChoiceValue.get_or_create(**defaults)
        attributes.append(attribute)
    return attributes


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


def create_product_types_by_schema(root_schema):
    results = []
    for product_type_name, schema in root_schema.items():
        product_type = create_product_type_with_attributes(product_type_name, schema)
        results.append((product_type, schema))
    return results


def set_product_attributes(product, product_type):
    attr_dict = {}
    for product_attribute in product_type.product_attributes:
        value = random.choice(product_attribute.values)
        attr_dict[str(product_attribute.id)] = str(value.id)

    product.attributes = attr_dict
    product.save()


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


def get_or_create_category(category_schema, placeholder_dir):
    if "parent" in category_schema:
        parent_id = get_or_create_category(
            category_schema["parent"], placeholder_dir
        ).id
    else:
        parent_id = 0
    category_name = category_schema["name"]
    image_name = category_schema["image_name"]
    image_dir = get_product_list_images_dir(placeholder_dir)
    defaults = {"background_img": str(image_dir / image_name)}
    category, _ = Category.get_or_create(
        title=category_name, parent_id=parent_id, **defaults
    )
    return category


def create_product(**kwargs):
    description = fake.paragraphs(5)
    defaults = {
        "title": fake.company(),
        "price": fake.pydecimal(2, 2, positive=True),
        "description": "\n\n".join(description),
        "is_featured": random.choice([0, 1]),
    }
    defaults.update(kwargs)
    return Product.create(**defaults)

def get_name_from_attributes(variant):
    """Generates ProductVariant's name based on its attributes."""
    values = [
        attributechoice_value.title
        for attributechoice_value in variant.attribute_map.values()
    ]
    return " / ".join(values)

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


def create_product_images(product, how_many, placeholder_dir):
    placeholder_root = Config.STATIC_DIR / placeholder_dir
    for dummy in range(how_many):
        image_name = random.choice(list(placeholder_root.iterdir()))
        image = str(image_name.relative_to(Config.STATIC_DIR))
        ProductImage.get_or_create(image=image, product_id=product.id)


def set_featured_products(how_many=8):
    pks = Product.objects.order_by("?")[:how_many].values_list("pk", flat=True)
    Product.objects.filter(pk__in=pks).update(is_featured=True)
    yield "Featured products created"


def get_product_list_images_dir(placeholder_dir):
    product_list_images_dir = placeholder_dir / "products-list"
    return product_list_images_dir


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
    page_data = {"content": content, "title": "About", "is_visible": True, "slug":"about"}
    page, _ = Page.get_or_create(**page_data)
    yield f"Page {page.title} created"


def generate_menu_items(category: Category, menu_id=None, parent_id=None):
    menu_item, created = MenuItem.get_or_create(
        title=category.title,
        category_id=category.id,
        site_id=menu_id,
        parent_id=parent_id,
    )

    if created:
        yield f"Created menu item for category {category}"

    for child in category.children:
        for msg in generate_menu_items(child, parent_id=menu_item.id):
            yield f"\t{msg}"


def create_menus():
    site = Site.query.first()
    if not site:
        site = Site.create(
            header_text="TEST SALEOR - A SAMPLE SHOP",
            description="sth about this site",
            top_menu_id=1,
            bottom_menu_id=2,
        )
    site.save()

    yield "Created navbar menu"
    categories = Category.query.all()
    for category in categories:
        if not category.parent_id:
            for msg in generate_menu_items(category, menu_id=1):
                yield msg

    yield "Created footer menu"
    collection = Collection.query.first()
    item, _ = MenuItem.get_or_create(title="Collections", site_id=2)
    for collection in Collection.query.all():
        MenuItem.get_or_create(
            title=collection.title, collection_id=collection.id, parent_id=item.id
        )

    item, _ = MenuItem.get_or_create(title="Saleor", site_id=2)
    page = Page.query.first()
    if page:
        MenuItem.get_or_create(title=page.title, page_id=page.id, parent_id=item.id)


def get_email(first_name, last_name):
    _first = unicodedata.normalize("NFD", first_name).encode("ascii", "ignore")
    _last = unicodedata.normalize("NFD", last_name).encode("ascii", "ignore")
    return (
        f"{_first.lower().decode('utf-8')}.{_last.lower().decode('utf-8')}@example.com"
    )


def create_users(how_many=10):
    for dummy in range(how_many):
        user = create_fake_user()
        yield f"User: {user.email}"


def create_fake_user():
    email = get_email(fake.first_name(), fake.last_name())
    user, _ = User.get_or_create(
        username=fake.first_name() + fake.last_name(),
        email=email,
        password="password",
        is_active=True,
    )
    return user


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


def create_addresses(how_many=10):
    for dummy in range(how_many):
        address = create_fake_address()
        yield f"Address: {address.contact_name}"


def create_shipping_methods():
    shipping_method = ShippingMethod.create(title="UPC", price=fake.money())
    yield f"Shipping method #{shipping_method.id}"
    shipping_method = ShippingMethod.create(title="DHL", price=fake.money())
    yield f"Shipping method #{shipping_method.id}"


def create_fake_collection(placeholder_dir, collection_data):
    image_dir = get_product_list_images_dir(placeholder_dir)
    background_img = image_dir / collection_data["image_name"]
    collection = Collection.get_or_create(
        title=collection_data["name"], background_img=str(background_img)
    )[0]
    products = Product.query.limit(4)
    for product in products:
        ProductCollection.create(product_id=product.id, collection_id=collection.id)
    return collection


def create_collections_by_schema(placeholder_dir, schema=COLLECTIONS_SCHEMA):
    for collection_data in schema:
        collection = create_fake_collection(placeholder_dir, collection_data)
        yield f"Collection: {collection}"


def create_admin():
    user = User.create(
        username="hjlarry",
        email="hjlarry@163.com",
        password="123",
        is_active=True,
        is_admin=True,
    )
    address1 = create_fake_address(user.id)
    address2 = create_fake_address(user.id)
    address3 = create_fake_address(user.id)
    yield f"Admin {user.username} created"


def create_payment(order):
    status = random.choice(
        [PAYMENT_STATUS_WAITING, PAYMENT_STATUS_PREAUTH, PAYMENT_STATUS_CONFIRMED]
    )
    payment = OrderPayment.create(
        order_id=order.id,
        status=status,
        total=order.total_net,
        delivery=order.shipping_price_net,
        customer_ip_address=fake.ipv4(),
    )
    return payment


def create_order_line(order, discounts, taxes):
    product = Product.query.order_by(func.random()).first()
    variant = product.variant[0]
    quantity = random.randrange(1, 5)
    variant.quantity += quantity
    variant.save()
    return OrderLine.create(
        order_id=order.id,
        product_name=variant.display_product(),
        product_sku=variant.sku,
        is_shipping_required=variant.is_shipping_required,
        quantity=quantity,
        variant_id=variant.id,
        unit_price_net=variant.price,
    )


def create_order_lines(order, discounts, taxes, how_many=10):
    for dummy in range(how_many):
        yield create_order_line(order, discounts, taxes)


def create_fake_order(discounts, taxes):
    user = User.query.filter_by(is_admin=False).order_by(func.random()).first()
    address = create_fake_address()
    order_data = {"user_id": user.id, "shipping_address_id": address.id}
    shipping_method = ShippingMethod.query.order_by(func.random()).first()
    order_data.update(
        {
            "shipping_method_name": shipping_method.title,
            "shipping_price_net": shipping_method.price,
        }
    )

    order = Order.create(**order_data)
    lines = create_order_lines(order, discounts, taxes, random.randrange(1, 5))
    order.total_net = sum(
        [line.get_total() for line in lines], order.shipping_price_net
    )
    order.save()
    create_payment(order)
    return order


def create_fake_sale():
    sale = Sale.create(
        title=f"Happy {fake.word()} day!",
        type=TYPE_PERCENT,
        value=random.choice([10, 20, 30, 40, 50]),
    )
    for product in Product.query.order_by(func.random()).all()[:4]:
        SaleProduct.create(sale_id=sale.id, product_id=product.id)
    return sale


def create_orders(how_many=10):
    taxes = None
    # discounts = Sale.objects.prefetch_related('products', 'categories')
    discounts = None
    for dummy in range(how_many):
        order = create_fake_order(discounts, taxes)
        yield f"Order: {order}"


def create_product_sales(how_many=5):
    for dummy in range(how_many):
        sale = create_fake_sale()
        yield f"Sale: {sale}"


def create_vouchers():
    defaults = {
        "type": VOUCHER_TYPE_SHIPPING,
        "title": "Free shipping",
        "discount_value_type": TYPE_PERCENT,
        "discount_value": 100,
    }
    voucher, created = Voucher.get_or_create(code="FREESHIPPING", **defaults)
    if created:
        yield f"Voucher #{voucher.id}"
    else:
        yield "Shipping voucher already exists"

    defaults = {
        "type": VOUCHER_TYPE_VALUE,
        "title": "Big order discount",
        "discount_value_type": TYPE_FIXED,
        "discount_value": 25,
        "limit": 200,
    }

    voucher, created = Voucher.get_or_create(code="DISCOUNT", **defaults)
    if created:
        yield f"Voucher #{voucher.id}"
    else:
        yield "Value voucher already exists"


dashboard_menus = [
    {"title": "User", "endpoint": "dashboard.users", "icon_cls": "fa-user"},
    {"title": "Product", "icon_cls": "fa-bandcamp"},
    {
        "title": "Order",
        "endpoint": "dashboard.orders",
        "icon_cls": "fa-cart-arrow-down",
    },
    {"title": "Promotion", "icon_cls": "fa-gratipay"},
    {"title": "Site", "icon_cls": "fa-cog"},
    {"title": "ProductList", "endpoint": "dashboard.products", "parent_id":2},
    {"title": "Type", "endpoint": "dashboard.product_types", "parent_id":2},
    {"title": "Category", "endpoint": "dashboard.categories", "parent_id":2},
    {"title": "Collection", "endpoint": "dashboard.collections", "parent_id":2},
    {"title": "Attribute", "endpoint": "dashboard.attributes", "parent_id":2},
    {"title": "Page", "endpoint": "dashboard.site_pages", "parent_id":5},
    {"title": "SiteMenu", "endpoint": "dashboard.site_menus", "parent_id":5},
    {"title": "DashboardMenu", "endpoint": "dashboard.dashboard_menus", "parent_id":5},
]

def create_dashboard_menus():
    for item in dashboard_menus:
        DashboardMenu.create(**item)
    yield "create dashboard menus"