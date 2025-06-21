from pydantic import BaseModel
from enum import Enum

class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    CONCLUDED = "concluded"

class OrderStatusUpdate(BaseModel):
    status: OrderStatusEnum
