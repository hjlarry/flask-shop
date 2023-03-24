from flask_babel import lazy_gettext
from flask_wtf import FlaskForm as _FlaskForm
from flask_wtf.file import FileSize, FileAllowed
from wtforms import (
    BooleanField,
    DateTimeField,
    DateField,
    DecimalField,
    FieldList,
    FileField,
    MultipleFileField,
    FloatField,
    IntegerField,
    PasswordField,
    RadioField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Regexp, optional

from flaskshop.constant import Permission, SettingValueType


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
    title = StringField(lazy_gettext("Title"), validators=[DataRequired()])
    order = IntegerField(lazy_gettext("Order"), default=0)
    endpoint = StringField(lazy_gettext("End Point"))
    icon_cls = StringField(lazy_gettext("Icon"))
    parent_id = SelectField(lazy_gettext("Parent"))
    submit = SubmitField(lazy_gettext("Submit"))


class SiteMenuForm(FlaskForm):
    title = StringField(lazy_gettext("Title"), validators=[DataRequired()])
    order = IntegerField(lazy_gettext("Order"), default=0)
    url_ = StringField(lazy_gettext("Url"))
    parent_id = SelectField(lazy_gettext("Parent"))
    position = RadioField(
        lazy_gettext("Position"),
        choices=[
            (0, lazy_gettext("none")),
            (1, lazy_gettext("top")),
            (2, lazy_gettext("bottom")),
        ],
        default=0,
    )
    category_id = SelectField(lazy_gettext("Category"))
    collection_id = SelectField(lazy_gettext("Collection"))
    page_id = SelectField(lazy_gettext("Page"))
    submit = SubmitField(lazy_gettext("Submit"))


class SitePageForm(FlaskForm):
    title = StringField(lazy_gettext("Title"), validators=[DataRequired()])
    slug = StringField(
        lazy_gettext("Slug"),
        validators=[Regexp(r"^\D+$", message="slug can not be number")],
    )
    content = StringField(lazy_gettext("Content"))
    is_visible = BooleanField(lazy_gettext("Is Visible"), default=True)
    submit = SubmitField(lazy_gettext("Submit"))


class SiteConfigForm(FlaskForm):
    header_text = StringField(lazy_gettext("Header"), validators=[DataRequired()])
    description = TextAreaField(lazy_gettext("Description"))
    submit = SubmitField(lazy_gettext("Submit"))


class UserForm(FlaskForm):
    username = StringField(lazy_gettext("User Name"), validators=[DataRequired()])
    email = StringField(lazy_gettext("E-mail"), validators=[DataRequired()])
    password = PasswordField(lazy_gettext("Password"))
    is_active = BooleanField(lazy_gettext("Is Active"))
    role = SelectField(
        lazy_gettext("Role"),
        coerce=str,
        choices=list(Permission.PERMISSION_MAP.values()),
    )
    created_at = DateTimeField(lazy_gettext("Created at"))
    updated_at = DateTimeField(lazy_gettext("Updated at"))
    submit = SubmitField(lazy_gettext("Submit"))


class UserAddressForm(FlaskForm):
    province = StringField(lazy_gettext("Province"))
    city = StringField(lazy_gettext("Sity"))
    district = StringField(lazy_gettext("District"))
    address = StringField(lazy_gettext("Address"))
    contact_name = StringField(lazy_gettext("Contact Name"))
    contact_phone = StringField(lazy_gettext("Contact Phone"))
    submit = SubmitField(lazy_gettext("Submit"))


class AttributeForm(FlaskForm):
    title = StringField(lazy_gettext("Title"), validators=[DataRequired()])
    values_label = StringField(
        lazy_gettext("Value"),
        description=lazy_gettext("Multiple values need separated by ','"),
    )
    product_types_ids = SelectMultipleField(lazy_gettext("Product Types"))
    submit = SubmitField(lazy_gettext("Submit"))


class CollectionForm(FlaskForm):
    title = StringField(lazy_gettext("Title"), validators=[DataRequired()])
    products_ids = SelectMultipleField(lazy_gettext("Products"))
    background_img = StringField(lazy_gettext("Current Image"))
    bgimg_file = FileField(
        lazy_gettext("Upload a new one"),
        validators=[
            FileAllowed(["jpg", "png", "gif", "jpeg"], "Images only!"),
            FileSize(1024 * 1024 * 1024, message="It is too big!"),
        ],
    )
    submit = SubmitField(lazy_gettext("Submit"))


class CategoryForm(FlaskForm):
    title = StringField(lazy_gettext("Title"), validators=[DataRequired()])
    parent_id = SelectField(lazy_gettext("Parent"), coerce=int, default=0)
    background_img = StringField(lazy_gettext("Current Image"))
    bgimg_file = FileField(
        lazy_gettext("Upload a new one"),
        validators=[
            FileAllowed(["jpg", "png", "gif", "jpeg"], "Images only!"),
            FileSize(1024 * 1024 * 1024, message="It is too big!"),
        ],
    )
    submit = SubmitField(lazy_gettext("Submit"))


class ProductTypeForm(FlaskForm):
    title = StringField(lazy_gettext("Title"), validators=[DataRequired()])
    has_variants = BooleanField(lazy_gettext("Has variant"), default=True)
    is_shipping_required = BooleanField(
        lazy_gettext("Is shipping required"), default=True
    )
    product_attributes_ids = SelectMultipleField(lazy_gettext("Product atributes"))
    variant_attr_id = SelectField(lazy_gettext("Variant Attributes"))
    submit = SubmitField(lazy_gettext("Submit"))


class ProductForm(FlaskForm):
    title = StringField(lazy_gettext("Title"))
    basic_price = DecimalField(lazy_gettext("Basic Price"))
    on_sale = BooleanField(lazy_gettext("On Sale"), default=True)
    is_featured = BooleanField(lazy_gettext("Is Featured"), default=False)
    rating = FloatField(lazy_gettext("Rating"), default=0)
    sold_count = IntegerField(lazy_gettext("Sold Count"), default=0)
    review_count = IntegerField(lazy_gettext("Review Count"), default=0)
    category_id = SelectField(lazy_gettext("Category"))
    description = TextAreaField(lazy_gettext("Description"))
    images = FieldList(StringField(lazy_gettext("Images")))
    new_images = MultipleFileField(
        lazy_gettext(""),
        validators=[
            FileAllowed(["jpg", "png", "gif", "jpeg"], "Images only!"),
            FileSize(1024 * 1024 * 1024, message="It is too big!"),
            Length(max=5, message="You can only upload 5 images once"),
        ],
    )
    attributes = FieldList(SelectField(lazy_gettext("Atributes")))
    submit = SubmitField(lazy_gettext("Submit"))


class ProductCreateForm(FlaskForm):
    product_type_id = SelectField(lazy_gettext("Choose A Product Type"), default=1)
    submit = SubmitField(lazy_gettext("Next"))


class VariantForm(FlaskForm):
    sku_id = IntegerField(
        lazy_gettext("SKU"), validators=[DataRequired(), NumberRange(min=1, max=9999)]
    )
    title = StringField(lazy_gettext("Title"), validators=[DataRequired()])
    price_override = DecimalField(
        lazy_gettext("Price override"), default=0.00, validators=[NumberRange(min=0)]
    )
    quantity = IntegerField(
        lazy_gettext("Quantity"), default=0, validators=[NumberRange(min=0)]
    )
    submit = SubmitField(lazy_gettext("Submit"))


class ShippingMethodForm(FlaskForm):
    title = StringField(lazy_gettext("Title"), validators=[DataRequired()])
    price = DecimalField(
        lazy_gettext("Price"), default=0.00, validators=[NumberRange(min=0)]
    )
    submit = SubmitField(lazy_gettext("Submit"))


class VoucherForm(FlaskForm):
    title = StringField(lazy_gettext("Title"), validators=[DataRequired()])
    type_ = SelectField(lazy_gettext("Type"), default=1)
    code = StringField(lazy_gettext("Code"), validators=[DataRequired()])
    usage_limit = IntegerField(
        lazy_gettext("Usage limit"),
        description=lazy_gettext("how many times can be used"),
        validators=[optional()],
    )
    used = IntegerField(lazy_gettext("Used"), default=0)
    start_date = DateField(lazy_gettext("Start At"))
    end_date = DateField(lazy_gettext("End At"))
    discount_value_type = SelectField(lazy_gettext("Discount value type"), default=1)
    discount_value = DecimalField(lazy_gettext("Discount value"), default=0.00)
    limit = IntegerField(lazy_gettext("Limit"), validators=[optional()])
    category_id = SelectField(
        lazy_gettext("Category"),
        description=lazy_gettext("when type is category, need to select"),
    )
    product_id = SelectField(
        lazy_gettext("Product"),
        description=lazy_gettext("when type is product, need to select"),
    )
    submit = SubmitField(lazy_gettext("Submit"))


class SaleForm(FlaskForm):
    title = StringField(lazy_gettext("Title"), validators=[DataRequired()])
    discount_value_type = SelectField(lazy_gettext("Discount value type"), default=1)
    discount_value = DecimalField(lazy_gettext("Discount value"), default=0.00)
    categories_ids = SelectMultipleField(lazy_gettext("Category"), coerce=int)
    products_ids = SelectMultipleField(lazy_gettext("Product"))
    submit = SubmitField(lazy_gettext("Submit"))


def generate_settings_form(settings):
    """Generates a settings form which includes field validation
    based on our Setting Schema."""

    class SettingsForm(FlaskForm):
        pass

    # now parse the settings in this group
    for setting in settings:
        field_validators = []

        if setting.value_type in {SettingValueType.integer, SettingValueType.float}:
            validator_class = NumberRange
        elif setting.value_type == SettingValueType.string:
            validator_class = Length

        # generate the validators
        if setting.extra:
            if "min" in setting.extra:
                # Min number validator
                field_validators.append(validator_class(min=setting.extra["min"]))

            if "max" in setting.extra:
                # Max number validator
                field_validators.append(validator_class(max=setting.extra["max"]))

        # Generate the fields based on value_type
        # IntegerField
        if setting.value_type == SettingValueType.integer:
            setattr(
                SettingsForm,
                setting.key,
                IntegerField(
                    setting.name,
                    validators=field_validators,
                    description=setting.description,
                ),
            )
        # FloatField
        elif setting.value_type == SettingValueType.float:
            setattr(
                SettingsForm,
                setting.key,
                FloatField(
                    setting.name,
                    validators=field_validators,
                    description=setting.description,
                ),
            )

        # TextField
        elif setting.value_type == SettingValueType.string:
            setattr(
                SettingsForm,
                setting.key,
                StringField(
                    setting.name,
                    validators=field_validators,
                    description=setting.description,
                ),
            )

        # SelectMultipleField
        elif setting.value_type == SettingValueType.selectmultiple:
            # if no coerce is found, it will fallback to unicode
            if "coerce" in setting.extra:
                coerce_to = setting.extra["coerce"]
            else:
                coerce_to = str

            setattr(
                SettingsForm,
                setting.key,
                SelectMultipleField(
                    setting.name,
                    choices=setting.extra["choices"](),
                    coerce=coerce_to,
                    description=setting.description,
                ),
            )

        # SelectField
        elif setting.value_type == SettingValueType.select:
            # if no coerce is found, it will fallback to unicode
            if "coerce" in setting.extra:
                coerce_to = setting.extra["coerce"]
            else:
                coerce_to = str

            setattr(
                SettingsForm,
                setting.key,
                SelectField(
                    setting.name,
                    coerce=coerce_to,
                    choices=setting.extra["choices"](),
                    description=setting.description,
                ),
            )

        # BooleanField
        elif setting.value_type == SettingValueType.boolean:
            setattr(
                SettingsForm,
                setting.key,
                BooleanField(setting.name, description=setting.description),
            )

    SettingsForm.submit = SubmitField(lazy_gettext("Submit"))
    return SettingsForm
