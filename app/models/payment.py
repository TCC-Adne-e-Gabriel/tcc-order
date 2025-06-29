from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlmodel import (
    SQLModel, 
    Field, 
    Relationship
)
from app.schemas.payment import PaymentMethodEnum, PaymentStatusEnum
from typing import Optional

class Payment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    payment_method: PaymentMethodEnum
    order_id: UUID = Field(foreign_key="orders.id")
    status: PaymentStatusEnum
    paid_at: Optional[datetime] = None
    customer_id: UUID
    number_of_installments: int = 1
    total_amount: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    order: "Order" = Relationship(back_populates="payments")
