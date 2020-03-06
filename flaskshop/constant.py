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
    names="draft_created payment_captured payment_failed order_fully_paid canceled order_delivered",
)
DiscountValueTypeKinds = enum.Enum(value="DiscountValueType", names="fixed percent")
VoucherTypeKinds = enum.Enum(
    value="VoucherType", names="product category shipping value"
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
