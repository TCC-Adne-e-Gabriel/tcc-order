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
    status: PaymentStatusEnum = "pending"
    paid_at: Optional[datetime] = None
    customer_id: UUID
    number_of_installments: int = 1
    total_amount: Annotated[Decimal, AfterValidator(greater_than_zero)]
    
class PaymentUpdateRequest(BaseModel): 
    payment_method: Optional[PaymentMethodEnum]
    order_id: Optional[UUID]
    status: Optional[PaymentStatusEnum] = "pending"
    paid_at: Optional[datetime] = None
    customer_id: Optional[UUID]
    number_of_installments: int = 1
    total_amount: Annotated[Optional[Decimal], AfterValidator(greater_than_zero)]

class PaymentResponse(BaseModel): 
    id: UUID 
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True