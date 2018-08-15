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
    Collection
)
from flaskshop.public.models import Menu, Site, MenuItem, Page
from flaskshop.product.utils import get_name_from_attributes
from flaskshop.account.models import User, UserAddress
from flaskshop.checkout.models import ShippingMethod
from flaskshop.order.models import Order, OrderLine, OrderPayment
from flaskshop.discount.models import Voucher, Sale
from flaskshop.settings import Config
from flaskshop.constant import PAYMENT_STATUS_WAITING, PAYMENT_STATUS_PREAUTH, PAYMENT_STATUS_CONFIRMED, TYPE_PERCENT, \
    TYPE_FIXED, VOUCHER_TYPE_SHIPPING, VOUCHER_TYPE_VALUE

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


def create_attribute(**kwargs):
    # defaults = {"title": fake.word().title()}
    # defaults.update(kwargs)
    attribute, _ = ProductAttribute.get_or_create(**kwargs)
    return attribute


def create_attribute_value(attribute, **kwargs):
    defaults = {"attribute": attribute}
    defaults.update(kwargs)
    attribute_value, _ = AttributeChoiceValue.get_or_create(**defaults)
    return attribute_value


def create_attributes_and_values(attribute_data):
    attributes = []
    for attribute_name, attribute_values in attribute_data.items():
        attribute = create_attribute(title=attribute_name)
        for value in attribute_values:
            create_attribute_value(attribute, title=value)
        attributes.append(attribute)
    return attributes


def get_or_create_product_type(title, **kwargs):
    return ProductType.get_or_create(title=title, **kwargs)[0]


def create_product_type_with_attributes(name, schema):
    product_attributes_schema = schema.get("product_attributes", {})
    variant_attributes_schema = schema.get("variant_attributes", {})
    is_shipping_required = schema.get("is_shipping_required", True)
    product_type = get_or_create_product_type(
        title=name, is_shipping_required=is_shipping_required
    )
    product_attributes = create_attributes_and_values(product_attributes_schema)
    variant_attributes = create_attributes_and_values(variant_attributes_schema)

    product_type.product_attributes.extend(product_attributes)
    product_type.variant_attributes.extend(variant_attributes)
    product_type.save()
    return product_type


def create_product_types_by_schema(root_schema):
    results = []
    for product_type_name, schema in root_schema.items():
        product_type = create_product_type_with_attributes(product_type_name, schema)
        results.append((product_type, schema))
    return results


# above complete


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
        product = create_product(product_type=product_type, category=category)
        set_product_attributes(product, product_type)
        if create_images:
            type_placeholders = placeholder_dir / schema["images_dir"]
            create_product_images(product, random.randrange(1, 5), type_placeholders)
        variant_combinations = get_variant_combinations(product)

        prices = get_price_override(schema, len(variant_combinations), product.price)
        variants_with_prices = itertools.zip_longest(variant_combinations, prices)

        for i, variant_price in enumerate(variants_with_prices, start=1337):
            attr_combination, price = variant_price
            sku = "%s-%s" % (product.id, i)
            create_variant(
                product, attributes=attr_combination, sku=sku, price_override=price
            )

        if not variant_combinations:
            # Create min one variant for products without variant level attrs
            sku = "%s-%s" % (product.id, fake.random_int(1000, 100000))
            create_variant(product, sku=sku)
        if stdout is not None:
            stdout.write(
                "Product: %s (%s), %s variant(s)" % (product, product_type.name, 1)
            )


def create_products_by_schema(
        placeholder_dir, how_many, create_images, stdout=None, schema=DEFAULT_SCHEMA
):
    for product_type, type_schema in create_product_types_by_schema(schema):
        create_products_by_type(
            product_type,
            type_schema,
            placeholder_dir,
            how_many=how_many,
            create_images=create_images,
            stdout=stdout,
        )


def get_or_create_category(category_schema, placeholder_dir):
    if "parent" in category_schema:
        parent_id = get_or_create_category(
            category_schema["parent"], placeholder_dir
        ).id
    else:
        parent_id = None
    category_name = category_schema["name"]
    image_name = category_schema["image_name"]
    image_dir = get_product_list_images_dir(placeholder_dir)
    defaults = {"background_img": get_image(image_dir, image_name)}
    return Category.get_or_create(title=category_name, parent_id=parent_id, **defaults)[
        0
    ]


def create_product(**kwargs):
    description = fake.paragraphs(5)
    defaults = {
        "title": fake.company(),
        "price": fake.pydecimal(2, 2, positive=True),
        "description": "\n\n".join(description),
        "is_featured": random.choice([0, 1])
    }
    defaults.update(kwargs)
    return Product.create(**defaults)


def create_variant(product, **kwargs):
    defaults = {
        "product": product,
        "quantity": fake.random_int(1, 50),
        # "cost_price": fake.pydecimal(2, 2, positive=True),
        # "quantity_allocated": fake.random_int(1, 50),
    }
    defaults.update(kwargs)
    attributes = defaults.pop("attributes")
    variant = ProductVariant(**defaults)
    variant.attributes = attributes

    if variant.attributes:
        variant.title = get_name_from_attributes(variant)
    variant.save()
    return variant


def create_product_image(product, placeholder_dir):
    placeholder_root = Config.STATIC_DIR / placeholder_dir
    image_name = random.choice(list(placeholder_root.iterdir()))
    image = image_name.relative_to(Config.STATIC_DIR)
    product_image = ProductImage(product=product, image=image)
    product_image.save()
    # create_product_thumbnails.delay(product_image.pk)
    return product_image


def create_product_images(product, how_many, placeholder_dir):
    for dummy in range(how_many):
        create_product_image(product, placeholder_dir)


def set_featured_products(how_many=8):
    pks = Product.objects.order_by("?")[:how_many].values_list("pk", flat=True)
    Product.objects.filter(pk__in=pks).update(is_featured=True)
    yield "Featured products created"


def get_product_list_images_dir(placeholder_dir):
    product_list_images_dir = placeholder_dir / "products-list"
    return product_list_images_dir


def get_image(image_dir, image_name):
    img_path = image_dir / image_name
    # return File(open(img_path, "rb"))
    return img_path


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
    page_data = {"content": content, "title": "About", "is_visible": True}
    page, _ = Page.get_or_create(**page_data)
    yield "Page %s created" % page.title


def generate_menu_items(menu: Menu, category: Category, parent_menu_item):
    menu_item, created = MenuItem.get_or_create(
        title=category.title, category=category, parent=parent_menu_item
    )
    if not parent_menu_item:
        menu.items.append(menu_item)
        menu.save()

    if created:
        yield "Created menu item for category %s" % category

    for child in category.children:
        for msg in generate_menu_items(menu, child, menu_item):
            yield "\t%s" % msg


def generate_menu_tree(menu):
    categories = Category.query.all()
    for category in categories:
        if not category.parent_id:
            for msg in generate_menu_items(menu, category, None):
                yield msg


def create_menus():
    # Create navbar menu with category links
    top_menu, _ = Menu.get_or_create(title="top_menu")
    if not top_menu.items:
        yield "Created navbar menu"
        for msg in generate_menu_tree(top_menu):
            yield msg

    # Create footer menu with collections and pages
    bottom_menu, _ = Menu.get_or_create(title="bottom_menu")
    if not bottom_menu.items:
        collection = Collection.query.first()
        item, _ = MenuItem.get_or_create(
            title="Collections", collection=collection, menu=bottom_menu
        )

        for collection in Collection.query.all():
            MenuItem.get_or_create(
                title=collection.title, collection=collection, parent=item
            )

        page = Page.query.first()
        MenuItem.get_or_create(title=page.title, page=page)
        yield "Created footer menu"
    site = Site.query.first()
    if not site:
        site = Site.create(
            header_text="TEST SALEOR - A SAMPLE SHO", description="sth about this site"
        )

    site.top_menu = top_menu
    site.bottom_menu = bottom_menu
    site.save()


def get_email(first_name, last_name):
    _first = unicodedata.normalize("NFD", first_name).encode("ascii", "ignore")
    _last = unicodedata.normalize("NFD", last_name).encode("ascii", "ignore")
    return "%s.%s@example.com" % (
        _first.lower().decode("utf-8"),
        _last.lower().decode("utf-8"),
    )


def create_users(how_many=10):
    for dummy in range(how_many):
        user = create_fake_user()
        yield "User: %s" % (user.email,)


def create_fake_user():
    # address = create_address()
    email = get_email(fake.first_name(), fake.last_name())
    user, _ = User.get_or_create(
        username=fake.first_name() + fake.last_name(), email=email, password="password", active=True
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


def create_fake_address():
    address = UserAddress.create(
        contact_name=fake.name(),
        province=fake.state(),
        city=fake.city(),
        district=fake.city_suffix(),
        address=fake.street_address(),
        contact_phone=fake.phone_number(),
    )
    return address


def create_addresses(how_many=10):
    for dummy in range(how_many):
        address = create_fake_address()
        yield "Address: %s" % (address.contact_name,)


def create_shipping_methods():
    shipping_method = ShippingMethod.create(title="UPC", price=fake.money())
    yield "Shipping method #%d" % shipping_method.id
    shipping_method = ShippingMethod.create(title="DHL", price=fake.money())
    yield "Shipping method #%d" % shipping_method.id


def get_or_create_collection(title, placeholder_dir, image_name):
    background_img = get_image(placeholder_dir, image_name)
    return Collection.get_or_create(title=title, background_img=background_img)[0]


def create_fake_collection(placeholder_dir, collection_data):
    image_dir = get_product_list_images_dir(placeholder_dir)
    collection = get_or_create_collection(
        title=collection_data["name"],
        placeholder_dir=image_dir,
        image_name=collection_data["image_name"],
    )
    products = Product.query.limit(4)
    collection.products.extend(products)
    collection.save()
    return collection


def create_collections_by_schema(placeholder_dir, schema=COLLECTIONS_SCHEMA):
    for collection_data in schema:
        collection = create_fake_collection(placeholder_dir, collection_data)
        yield "Collection: %s" % (collection,)


def create_admin():
    address1 = create_fake_address()
    address2 = create_fake_address()
    address3 = create_fake_address()
    user = User.create(username='hjlarry', email='hjlarry@163.com', password='123', active=True, is_admin=True)
    user.addresses = [address1, address2, address3]
    user.save()
    yield f'Admin {user.username} created'


def create_payment(order):
    status = random.choice([PAYMENT_STATUS_WAITING, PAYMENT_STATUS_PREAUTH, PAYMENT_STATUS_CONFIRMED])
    payment = OrderPayment.create(
        order=order,
        status=status,
        total=order.total_net,
        delivery=order.shipping_price_net,
        customer_ip_address=fake.ipv4())
    return payment


# def create_fulfillments(order):
#     for line in order:
#         if random.choice([False, True]):
#             fulfillment, _ = Fulfillment.objects.get_or_create(order=order)
#             quantity = random.randrange(0, line.quantity) + 1
#             fulfillment.lines.create(order_line=line, quantity=quantity)
#             line.quantity_fulfilled = quantity
#             line.save(update_fields=['quantity_fulfilled'])
#
#     update_order_status(order)
def create_order_line(order, discounts, taxes):
    product = Product.query.order_by(func.random()).first()
    variant = product.variant[0]
    quantity = random.randrange(1, 5)
    variant.quantity += quantity
    variant.save()
    return OrderLine.create(
        order=order,
        product_name=variant.display_product(),
        product_sku=variant.sku,
        is_shipping_required=variant.is_shipping_required(),
        quantity=quantity,
        variant=variant,
        unit_price_net=variant.get_price(discounts=discounts, taxes=taxes),
    )


def create_order_lines(order, discounts, taxes, how_many=10):
    for dummy in range(how_many):
        yield create_order_line(order, discounts, taxes)


def create_fake_order(discounts, taxes):
    user = User.query.filter_by(is_admin=False).order_by(func.random()).first()

    order_data = {
        'user': user,
        'shipping_address': create_fake_address()}

    shipping_method = ShippingMethod.query.order_by(func.random()).first()

    order_data.update({
        'shipping_method_name': shipping_method.title,
        'shipping_price_net': shipping_method.price})

    order = Order.create(**order_data)

    lines = create_order_lines(order, discounts, taxes, random.randrange(1, 5))

    order.total_net = sum(
        [line.get_total() for line in lines], order.shipping_price_net)
    order.save()

    # create_fulfillments(order)

    create_payment(order)
    return order


def create_fake_sale():
    sale = Sale.create(
        title=f'Happy {fake.word()} day!',
        type=TYPE_PERCENT,
        value=random.choice([10, 20, 30, 40, 50]))
    for product in Product.query.order_by(func.random()).all()[:4]:
        sale.products.append(product)
    return sale


def create_orders(how_many=10):
    taxes = None
    # discounts = Sale.objects.prefetch_related('products', 'categories')
    discounts = None
    for dummy in range(how_many):
        order = create_fake_order(discounts, taxes)
        yield 'Order: %s' % (order,)


def create_product_sales(how_many=5):
    for dummy in range(how_many):
        sale = create_fake_sale()
        yield 'Sale: %s' % (sale,)


def create_vouchers():
    defaults = {
        'type': VOUCHER_TYPE_SHIPPING,
        'title': 'Free shipping',
        'discount_value_type': TYPE_PERCENT,
        'discount_value': 100}
    voucher, created = Voucher.get_or_create(
        code='FREESHIPPING', **defaults)
    if created:
        yield 'Voucher #%d' % voucher.id
    else:
        yield 'Shipping voucher already exists'

    defaults = {
        'type': VOUCHER_TYPE_VALUE,
        'title': 'Big order discount',
        'discount_value_type': TYPE_FIXED,
        'discount_value': 25,
        'limit': 200}

    voucher, created = Voucher.get_or_create(
        code='DISCOUNT', **defaults)
    if created:
        yield 'Voucher #%d' % voucher.id
    else:
        yield 'Value voucher already exists'

# def create_fake_group():
#     group, _ = Group.objects.get_or_create(name='Products Manager')
#     group.permissions.add(Permission.objects.get(codename='edit_product'))
#     group.permissions.add(Permission.objects.get(codename='view_product'))
#     group.save()
#     return group


# def create_groups():
#     group = create_fake_group()
#     return 'Group: %s' % (group.name,)
