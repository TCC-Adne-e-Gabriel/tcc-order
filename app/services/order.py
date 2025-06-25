from app.models.order import Order, OrderProduct
from app.schemas.order import OrderCreateRequest, OrderResponse, OrderUpdateRequest, OrderStatusUpdate, Product
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from app.exceptions import OrderNotFound
from app.clients.customer_client import CustomerClient
from app.clients.product_client import ProductClient


class OrderService():
    def __init__(self):
        self.customer_client = CustomerClient()
        self.product_client = ProductClient()

    async def create_order(self, session: Session, order: OrderCreateRequest) -> OrderResponse:
        total_price = 0
        order_products = []
        products = []
        for item in order.products:
            product: Product = await self.product_client.get_product_by_id(item.product_id, item.quantity)
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
        db_order = Order(**order_data)
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return OrderResponse.from_order(db_order, products)
    
    async def get_products_from_order(self, current_order: Order) -> List[Product]:
        products = []
        for item in current_order.products: 
            product: Product = await self.product_client.get_product_by_id(item.product_id, item.quantity)
            products.append(product)
        return products

    async def update_order(self, session: Session, order: OrderUpdateRequest, order_id: UUID):
        current_order = self.get_order_by_id(session, order_id)
        products = await self.get_products_from_order(current_order=current_order)
        order_db = order.model_dump(exclude_none=True)
        current_order.sqlmodel_update(order_db)
        session.add(current_order)
        session.commit()
        session.refresh(current_order)
        return OrderResponse.from_order(current_order, products)

    def get_orders_from_customer(self, customer_id: UUID) -> List[OrderResponse]: 
        self.customer_client.get_user_by_id(str(customer_id))
        return select(Order).where(Order.customer_id == customer_id)

    def get_order_by_id(self, session: Session, order_id: UUID) -> Order: 
        statement = select(Order).where(Order.id == order_id)
        order = session.exec(statement).first()
        if not order:
            raise OrderNotFound
        return order

    def get_orders(self, session: Session) -> List[OrderResponse]: 
        statement = select(Order).where(Order)
        return session.exec(statement).all()

    def delete_order(self, session: Session, order_id):
        current_order = self.get_order_by_id(session=session, order_id=order_id) 
        session.delete(current_order)
        session.commit()

    def update_order_status(self, session: Session, status_update: OrderStatusUpdate, order_id: UUID):
        current_order = self.get_order_by_id(session, order_id)
        order_db = OrderStatusUpdate(status=status_update.status).model_dump()
        current_order.sqlmodel_update(order_db)
        session.add(current_order)
        session.commit()
        session.refresh(current_order)
        return current_order