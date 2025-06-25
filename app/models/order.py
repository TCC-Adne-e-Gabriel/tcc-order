from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel
from uuid import UUID, uuid4
from enum import Enum

class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    CONCLUDED = "concluded"

class Order(SQLModel, table=True):
    __tablename__ = "orders"  

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    customer_id: UUID
    freight: float
    status: OrderStatusEnum
    total_price: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    products: List["OrderProduct"] = Relationship(back_populates="order")
    payments: List["Payment"] = Relationship(back_populates="order")


class OrderProduct(SQLModel, table=True):
    order_id: UUID = Field(foreign_key="orders.id", primary_key=True)
    product_id: UUID = Field(primary_key=True)
    quantity: float
    unit_price: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    order: Optional[Order] = Relationship(back_populates="products")