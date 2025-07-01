from pydantic import BaseModel, AfterValidator 
from uuid import UUID
from fastapi import UploadFile, File
from datetime import datetime
from typing import Optional, Annotated, List
from decimal import Decimal
from app.models.order import Order, OrderStatusEnum
from app.utils import greater_than_zero

class ProductOrder(BaseModel): 
    product_id: UUID
    quantity: int

class Product(BaseModel):
    name: str
    description: str
    price: Decimal
    sku: str
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: OrderStatusEnum

class OrderCreateRequest(BaseModel): 
    freight: Decimal
    products: List[ProductOrder]
    status: Optional[OrderStatusEnum] = "pending"

class OrderUpdateRequest(BaseModel): 
    customer_id: Optional[UUID] = None
    freight: Optional[Decimal] = None
    status: Optional[OrderStatusEnum] = None
    total_price: Optional[Annotated[Decimal, AfterValidator(greater_than_zero)]] = None

class OrderSimpleResponse(OrderCreateRequest): 
    id: UUID 
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OrderResponse(OrderCreateRequest): 
    id: UUID 
    created_at: datetime
    updated_at: datetime
    products: List[Product]
    class Config:
        from_attributes = True

    @classmethod
    def from_order(cls, order: Order, products: List[Product]): 
        return cls(
            id=order.id, 
            created_at=order.created_at, 
            updated_at=order.updated_at, 
            products=products,
            freight=order.freight, 
            status=order.status,
            customer_id=order.customer_id
        )

class Message(BaseModel): 
    message: str

class UpdateQuantityRequest(BaseModel): 
    quantity: int