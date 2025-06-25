from app.models.order import Order
from app.schemas.order import OrderCreateRequest, OrderResponse, OrderUpdateRequest, OrderStatusUpdate
from sqlmodel import Session, select
from app.core.encrypt import encrypt_data
from uuid import UUID
from exceptions import OrderNotFound
from clients.customer_client import CustomerClient
from clients.product_client import ProductClient()


class OrderService():
    def __init__(session: Session, self):
        self.customer_client = CustomerClient()
        self.product_client = ProductClient()

    def create_order(self, session: Session, order: OrderCreateRequest) -> OrderResponse:
        for item_data in order.products:
            product = 

        
        order_data = order.model_dump()
        db_order = Order(**order_data)
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return db_order

    def update_customer(self, session: Session, customer: OrderUpdateRequest, order_id: UUID):
        current_customer = self.get_order_by_id(order_id)
        customer_db = customer.model_dump(exclude_none=True)
        current_customer.sqlmodel_update(customer_db)
        session.add(current_customer)
        session.commit()
        session.refresh(current_customer)
        return current_customer

    def get_orders_from_customer(self, customer_id: UUID): 
        self.customer_client.get_user_by_id(str(customer_id))
        return select(Order).where(Order.customer_id == customer_id)

    def get_order_by_id(self, session: Session, order_id: UUID) -> Order: 
        statement = select(Order).where(Order.id == order_id)
        order = session.exec(statement).first()
        if not order:
            raise OrderNotFound

    def get_orders(self, session: Session): 
        statement = select(Order).where(Order)

    def delete_order(self, session: Session, order_id):
        current_order = self.get_order_by_id(session=session, order_id=order_id) 
        session.delete(current_order)
        session.commit()

    def update_order_status(self, status_update: OrderStatusUpdate):
        order_db = OrderStatusUpdate(status=status_update.status).model_dump()
        current_order.sqlmodel_update(order_db)
        session.add(current_order)
        session.commit()
        session.refresh(current_order)
        return current_order