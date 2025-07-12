from app.models.order import Order, OrderProduct
from app.schemas.order import (
    OrderCreateRequest, 
    OrderResponse, 
    OrderUpdateRequest, 
    OrderStatusUpdate, 
    Product, 
    OrderSimpleResponse
)
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from app.exceptions import OrderNotFoundException, OrderProductException
from app.clients.customer_client import CustomerClient
from app.clients.product_client import ProductClient
from app.order_logging import logger

class OrderService():
    def __init__(self):
        self.customer_client = CustomerClient()
        self.product_client = ProductClient()

    async def create_order(self, session: Session, order: OrderCreateRequest, customer_id: UUID) -> OrderResponse:
        total_price = 0
        order_products = []
        products = []
        for item in order.products:
            product: Product = await self.product_client.fetch_product(item.product_id, item.quantity)
            total_price += product.price * item.quantity
            products.append(product)
            order_product = OrderProduct(
                product_id=product.id, 
                quantity=item.quantity,
                unit_price=product.price
            )
            order_products.append(order_product)

        order_data = order.model_dump()
        order_data["total_price"] = total_price
        order_data["products"] = order_products
        order_data["customer_id"] = customer_id
        db_order = Order(**order_data)
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        logger.audit(f"Order {db_order.id} created")
        return OrderResponse.from_order(db_order, products)
    
    async def read_products_from_order(self, current_order: Order) -> List[Product]:
        products = []
        for item in current_order.products: 
            product: Product = await self.product_client.fetch_product(item.product_id, item.quantity)
            products.append(product)
        return products

    async def update_order(self, session: Session, order: OrderUpdateRequest, order_id: UUID):
        current_order = self.get_by_id(session, order_id)
        products = await self.read_products_from_order(current_order=current_order)
        order_db = order.model_dump(exclude_none=True)
        current_order.sqlmodel_update(order_db)
        session.add(current_order)
        session.commit()
        session.refresh(current_order)
        logger.audit(f"Order {current_order.id} updated")
        return OrderResponse.from_order(current_order, products)
    
    async def to_response_schema(self, orders) -> List[OrderResponse]: 
        orders_response = []

        for order in orders:
            products =  await self.read_products_from_order(order)
            orders_response.append(OrderResponse.from_order(order, products))
        return orders_response

    async def read_customer_orders(self, session: Session, customer_id: UUID) -> List[OrderResponse]: 
        await self.customer_client.read_user_by_id(str(customer_id))
        orders = session.exec(select(Order).where(Order.customer_id == customer_id))
        logger.audit(f"Orders from {customer_id} read")
        return await self.to_response_schema(orders)

    def get_by_id(self, session: Session, order_id: UUID) -> Order: 
        statement = select(Order).where(Order.id == order_id)
        result = session.exec(statement).first()
        
        return result

    async def read_order_by_id(self, session: Session, order_id: UUID) -> OrderResponse: 
        order = self.get_by_id(session, order_id)
        products = await self.read_products_from_order(order)
        if not order:
            raise OrderNotFoundException
        logger.audit(f"Order {order.id} read")
        return OrderResponse.from_order(order, products)

    async def read_orders(self, session: Session) -> List[OrderResponse]: 
        statement = select(Order)
        orders = session.exec(statement)

        logger.audit(f"Orders read")
        return await self.to_response_schema(orders)

    def delete_order(self, session: Session, order_id):
        current_order = self.get_by_id(session=session, order_id=order_id) 
        statement = select(OrderProduct).where(OrderProduct.order_id == order_id)
        order_products = session.exec(statement).all()
        
        for item in order_products: 
            session.delete(item)

        session.delete(current_order)
        session.commit()
        logger.audit(f"Order {order_id} deleted")

    def update_order_status(self, session: Session, status_update: OrderStatusUpdate, order_id: UUID) -> OrderSimpleResponse:
        current_order = self.get_by_id(session, order_id)
        order_db = OrderStatusUpdate(status=status_update.status).model_dump()
        current_order.sqlmodel_update(order_db)
        session.add(current_order)
        session.commit()
        session.refresh(current_order)
        logger.audit(f"Order status {order_id} updated")
        return current_order