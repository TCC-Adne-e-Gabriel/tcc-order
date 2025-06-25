from pydantic import BaseModel, AfterValidator 
from enum import Enum
from uuid import UUID
from datetime import datetime
from typing import Optional, Annotated, List
from decimal import Decimal
from app.utils import greater_than_zero

class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    CONCLUDED = "concluded"

class OrderStatusUpdate(BaseModel):
    status: OrderStatusEnum

class OrderCreateRequest(BaseModel): 
    customer_id: UUID
    freight: Decimal
    status: OrderStatusEnum
    total_price: Annotated[Decimal, AfterValidator(greater_than_zero)]
    products: List[UUID]


class OrderUpdateRequest(BaseModel): 
    customer_id: Optional[UUID]
    freight: Optional[Decimal]
    status: OrderStatusEnum
    total_price: Annotated[Optional[Decimal], AfterValidator(greater_than_zero)]
    products: Optional[List[UUID]]

class OrderResponse(BaseModel): 
    id: UUID 
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Message(BaseModel): 
    message: str