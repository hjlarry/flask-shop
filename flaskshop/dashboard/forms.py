from flask_wtf import FlaskForm as _FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SubmitField,
    SelectField,
    RadioField,
    TextAreaField,
    BooleanField,
    PasswordField,
    FieldList,
    SelectMultipleField,
    FileField,
    FloatField,
    DecimalField,
    DateTimeField,
)
from wtforms.validators import DataRequired, optional, NumberRange


class FlaskForm(_FlaskForm):
    def validate(self, extra_validators=None):
        self._errors = None
        success = True
        for name, field in self._fields.items():
            if field.type in (
                "SelectField",
                "SelectMultipleField",
                "RadioField",
                "FieldList",
            ):
                continue
            if extra_validators is not None and name in extra_validators:
                extra = extra_validators[name]
            else:
                extra = tuple()
            if not field.validate(self, extra):
                success = False
        return success


class DashboardMenuForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    order = IntegerField(default=0)
    endpoint = StringField()
    icon_cls = StringField()
    parent_id = SelectField("Parent")
    submit = SubmitField()


class SiteMenuForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    order = IntegerField(default=0)
    url_ = StringField("Url")
    parent_id = SelectField("Parent")
    site_id = RadioField("Position", choices=[(0, "none"), (1, "top"), (2, "bottom")], default=0)
    category_id = SelectField("Category")
    collection_id = SelectField("Collection")
    page_id = SelectField("Page")
    submit = SubmitField()


class SitePageForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    slug = StringField()
    content = TextAreaField()
    is_visible = BooleanField(default=True)
    submit = SubmitField()


class SiteConfigForm(FlaskForm):
    header_text = StringField(validators=[DataRequired()])
    description = TextAreaField()
    submit = SubmitField()


class UserForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    password = PasswordField()
    is_active = BooleanField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    submit = SubmitField()


class UserAddressForm(FlaskForm):
    province = StringField()
    city = StringField()
    district = StringField()
    address = StringField()
    contact_name = StringField()
    contact_phone = StringField()
    submit = SubmitField()


class AttributeForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    values = FieldList(StringField("Value"))
    types = SelectMultipleField("Product Types")
    submit = SubmitField()


class CollectionForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    products = SelectMultipleField()
    background_img = StringField("Current Image")
    bgimg_file = FileField("Upload")
    submit = SubmitField()


class CategoryForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    parent_id = SelectField("Parent")
    background_img = StringField("Current Image")
    bgimg_file = FileField("Upload")
    submit = SubmitField()


class ProductTypeForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    has_variants = BooleanField(default=True)
    is_shipping_required = BooleanField(default=True)
    product_attributes = SelectMultipleField()
    variant_attr_id = SelectField("Variant Attributes")
    submit = SubmitField()


class ProductForm(FlaskForm):
    title = StringField()
    basic_price = DecimalField()
    on_sale = BooleanField(default=True)
    is_featured = BooleanField(default=False)
    rating = FloatField(default=0)
    sold_count = IntegerField(default=0)
    review_count = IntegerField(default=0)
    category_id = SelectField()
    description = TextAreaField()
    images = FieldList(StringField())  # TODO 限制图片数量
    attributes = FieldList(SelectField())
    submit = SubmitField()


class ProductCreateForm(FlaskForm):
    product_type_id = SelectField("Choose A Product Type", default=1)
    submit = SubmitField()


class VariantForm(FlaskForm):
    sku_id = IntegerField("SKU", validators=[DataRequired(), NumberRange(min=1, max=9999)])
    title = StringField(validators=[DataRequired()])
    price_override = DecimalField(default=0.00, validators=[NumberRange(min=0)])
    quantity = IntegerField(default=0, validators=[NumberRange(min=0)])
    submit = SubmitField()


class VoucherForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    type_ = SelectField(default=1)
    code = StringField(validators=[DataRequired()])
    usage_limit = IntegerField(
        description="how many times can be used", validators=[optional()]
    )
    used = IntegerField(default=0)
    validity_period = StringField()
    discount_value_type = SelectField(default=1)
    discount_value = DecimalField(default=0.00)
    limit = IntegerField(validators=[optional()])
    category_id = SelectField(
        "Category", description="when type is category, need to select"
    )
    product_id = SelectField(
        "Product", description="when type is product, need to select"
    )
    submit = SubmitField()

class SaleForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    discount_value_type = SelectField(default=1)
    discount_value = DecimalField(default=0.00)
    categories = SelectMultipleField("Category")
    products = SelectMultipleField("Product")
    submit = SubmitField()
