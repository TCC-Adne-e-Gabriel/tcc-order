from enum import Enum
from pydantic import BaseModel, AfterValidator, BaseModel
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, Annotated
from decimal import Decimal
from app.utils import greater_than_zero

class PaymentMethodEnum(str, Enum):
    credit_card = "credit_card"
    boleto = "boleto"
    pix = "pix"

class PaymentStatusEnum(str, Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    cancelled = "cancelled"

class PaymentCreateRequest(BaseModel): 
    payment_method: PaymentMethodEnum
    order_id: UUID
    status: PaymentStatusEnum = PaymentStatusEnum.pending
    paid_at: Optional[datetime] = None
    number_of_installments: int = 1
    total_amount: Annotated[Decimal, AfterValidator(greater_than_zero)]
    
class PaymentUpdateRequest(BaseModel): 
    payment_method: Optional[PaymentMethodEnum] = None
    order_id: Optional[UUID] = None
    status: Optional[PaymentStatusEnum] = None
    paid_at: Optional[datetime] = None
    customer_id: Optional[UUID] = None
    number_of_installments: Optional[int] = None
    total_amount: Optional[Annotated[Decimal, AfterValidator(greater_than_zero)]] = None

class PaymentResponse(PaymentCreateRequest): 
    id: UUID 
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True