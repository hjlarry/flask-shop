import enum

ShipStatusKinds = enum.Enum(value="ShipStatus", names="pending delivered received")
PaymentStatusKinds = enum.Enum(
    value="PaymentStatus", names="waiting preauth confirmed rejected"
)
OrderStatusKinds = enum.Enum(
    value="OrderStatus", names="draft unfulfilled fulfilled canceled completed shipped"
)
OrderEvents = enum.Enum(
    value="OrderEvents",
    names="draft_created payment_captured payment_failed order_canceled order_delivered order_completed",
)
DiscountValueTypeKinds = enum.Enum(value="DiscountValueType", names="fixed percent")
VoucherTypeKinds = enum.Enum(
    value="VoucherType", names="product category shipping value"
)

SettingValueType = enum.Enum(
    value="SettingValueType", names="string integer float boolean select selectmultiple"
)


class Permission:
    LOGIN = 0x01
    EDITOR = 0x02
    OPERATOR = 0x04
    ADMINISTER = 0xFF
    PERMISSION_MAP = {
        LOGIN: ("login", "Login user"),
        EDITOR: ("editor", "Editor"),
        OPERATOR: ("op", "Operator"),
        ADMINISTER: ("admin", "Super administrator"),
    }


SiteDefaultSettings = {
    "project_title": {
        "value": "FlaskShop",
        "value_type": SettingValueType.string,
        "name": "Project title",
        "description": "The title of the project.",
    },
    "project_subtitle": {
        "value": "A lightweight e-commerce software in Flask",
        "value_type": SettingValueType.string,
        "name": "Project subtitle",
        "description": "A short description of the project.",
    },
    "project_copyright": {
        "value": "COPYRIGHT © 2009–2019 MIRUMEE SOFTWARE",
        "value_type": SettingValueType.string,
        "name": "Project Copyright",
        "description": "Copyright notice of the Project like '&copy; 2019 FlaskShop'. ",
    },
}
