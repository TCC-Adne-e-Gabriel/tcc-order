from app.models.payment import Payment
from app.schemas.payment import (
    PaymentCreateRequest, 
    PaymentResponse, 
    PaymentUpdateRequest
)
from sqlmodel import Session, select
from app.core.encrypt import encrypt_data
from uuid import UUID
from app.services.order import OrderService
from app.clients.customer_client import CustomerClient
from app.exceptions import *
from http import HTTPStatus


class PaymentService():
    def __init__(self):
        self.customer_client = CustomerClient()
        self.order_service = OrderService()

    async def create_payment(self, session: Session, payment: PaymentCreateRequest, customer_id: UUID) -> PaymentResponse:
        await self.customer_client.fetch_user(customer_id)
        self.order_service.read_order_by_id(session=session, order_id=payment.order_id)
        payment_data = payment.model_dump()
        payment_data["customer_id"] = customer_id
        db_payment = Payment(**payment_data)
        session.add(db_payment)
        session.commit()
        session.refresh(db_payment)
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
        return current_payment

    def read_payment_from_id(self, session: Session, payment_id: UUID) -> PaymentResponse: 
        statement = select(Payment).where(Payment.id == payment_id)
        payment = session.exec(statement).first()
        if not payment:
            raise PaymentNotFoundException(status_code=HTTPStatus.NOT_FOUND, detail="Payment not found")
        return payment
    
    async def read_customer_payments(self, session: Session, customer_id: UUID) -> PaymentResponse: 
        await self.customer_client.fetch_user(str(customer_id))
        statement = select(Payment).where(Payment.customer_id == customer_id)
        return session.exec(statement).all()

    def read_order_payments(self, session: Session, order_id: UUID) -> PaymentResponse: 
        self.order_service.read_order_by_id(session=session, order_id=order_id)
        statement = select(Payment).where(Payment.order_id == order_id)
        return session.exec(statement).all()

    def read_payments(self, session: Session) -> PaymentResponse: 
        statement = select(Payment)
        return session.exec(statement).all()

    def delete_payment(self, session: Session, payment_id: UUID): 
        current_payment = self.read_payment_from_id(session, payment_id)
        session.delete(current_payment)
        session.commit()
    


