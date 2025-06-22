from enum import Enum

class PaymentMethodEnum(str, Enum):
    credit_card = "credit_card"
    boleto = "boleto"
    pix = "pix"

class PaymentStatusEnum(str, Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    cancelled = "cancelled"
