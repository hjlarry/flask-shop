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
)
from wtforms.validators import DataRequired


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
    site_id = RadioField("Position", choices=[(1, "top"), (2, "bottom")])
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


class UserForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    password = PasswordField()
    is_active = BooleanField()
    is_admin = BooleanField()
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
    title = StringField()
    values = FieldList(StringField("Value"))
    types = SelectMultipleField("Product Types")
    submit = SubmitField()


class CollectionForm(FlaskForm):
    title = StringField()
    products = SelectMultipleField()
    background_img = StringField("Current Image")
    bgimg_file = FileField("Upload")
    submit = SubmitField()


class CategoryForm(FlaskForm):
    title = StringField()
    parent_id = SelectField("Parent")
    background_img = StringField("Current Image")
    bgimg_file = FileField("Upload")
    submit = SubmitField()


class ProductTypeForm(FlaskForm):
    title = StringField()
    has_variants = BooleanField(default=True)
    is_shipping_required = BooleanField(default=True)
    product_attributes = SelectMultipleField()
    variant_attr_id = SelectField("Variant Attributes")
    submit = SubmitField()


class ProductForm(FlaskForm):
    title = StringField()
    price = DecimalField()
    on_sale = BooleanField(default=True)
    is_featured = BooleanField(default=False)
    rating = FloatField(default=0)
    sold_count = IntegerField(default=0)
    review_count = IntegerField(default=0)
    category_id = SelectField()
    description = TextAreaField()
    images = FieldList(StringField())  # TODO 限制图片数量
    attributes = FieldList(SelectField())  # TODO
    submit = SubmitField()


class ProductCreateForm(FlaskForm):
    product_type_id = SelectField("Choose A Product Type")
    submit = SubmitField()


class VariantForm(FlaskForm):
    sku = StringField()
    title = StringField()
    price_override = DecimalField(default=0.00)
    quantity = IntegerField(default=0)
    submit = SubmitField()
