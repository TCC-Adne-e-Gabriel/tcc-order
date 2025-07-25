from app.models.payment import Payment
from app.schemas.payment import (
    PaymentCreateRequest, 
    PaymentResponse, 
    PaymentUpdateRequest
)
from sqlmodel import Session, select
from uuid import UUID
from app.services.order import OrderService
from app.clients.customer_client import CustomerClient
from app.exceptions import (
    PaymentNotFoundException
)
from app.order_logging import logger


class PaymentService():
    def __init__(self):
        self.customer_client = CustomerClient()
        self.order_service = OrderService()

    async def create_payment(self, session: Session, payment: PaymentCreateRequest) -> PaymentResponse:
        await self.customer_client.fetch_user(payment.customer_id)
        self.order_service.read_order_by_id(session=session, order_id=payment.order_id)
        payment_data = payment.model_dump()
        db_payment = Payment(**payment_data)
        session.add(db_payment)
        session.commit()
        session.refresh(db_payment)

        logger.audit(f"Payment {db_payment.id} created")
        return db_payment

    def update_payment(self, session: Session, payment: PaymentUpdateRequest, payment_id: UUID) -> PaymentResponse:
        current_payment = self.read_payment_from_id(
            session=session, 
            payment_id=payment_id
        )
        payment_db = payment.model_dump(exclude_none=True)
        current_payment.sqlmodel_update(payment_db)
        session.add(current_payment)
        session.commit()
        session.refresh(current_payment)
        logger.audit(f"Payment {current_payment.id} created")

        return current_payment

    def read_payment_from_id(self, session: Session, payment_id: UUID) -> PaymentResponse: 
        statement = select(Payment).where(Payment.id == payment_id)
        payment = session.exec(statement).first()
        if not payment:
            raise PaymentNotFoundException
        logger.audit(f"Payment {payment.id} read")
        return payment
    
    async def read_customer_payments(self, session: Session, customer_id: UUID) -> PaymentResponse: 
        await self.customer_client.fetch_user(str(customer_id))
        statement = select(Payment).where(Payment.customer_id == customer_id)
        payments = session.exec(statement).all()
        logger.audit(f"Payments from customer {customer_id} read")
        return payments

    def read_order_payments(self, session: Session, order_id: UUID) -> PaymentResponse: 
        self.order_service.read_order_by_id(session=session, order_id=order_id)
        statement = select(Payment).where(Payment.order_id == order_id)
        payments = session.exec(statement).all()
        logger.audit(f"Payments from order {order_id} read")
        return payments

    def read_payments(self, session: Session) -> PaymentResponse: 
        statement = select(Payment)
        payments = session.exec(statement).all()
        return payments

    def delete_payment(self, session: Session, payment_id: UUID): 
        current_payment = self.read_payment_from_id(session, payment_id)
        session.delete(current_payment)
        logger.audit(f"Payment {payment_id} deleted")
        session.commit()
    


