from fastapi import FastAPI
from fastapi import APIRouter, HTTPException
from app.services.payment_mock import PaymentMockService
from uuid import UUID, uuid4
from typing import List
from app.services.payment import PaymentService
from app.exceptions import PaymentNotFoundException, UserNotFoundException, OrderNotFound
from app.schemas.payment import PaymentResponse, PaymentCreateRequest, PaymentUpdateRequest
from app.models.payment import PaymentStatusEnum, PaymentMethodEnum
from app.deps import SessionDep
from http import HTTPStatus

app = FastAPI()
router = APIRouter(prefix="/payment")
payment_mock = PaymentMockService()
payment_service = PaymentService()

@router.get("/{id}/")
def get_payment_by_id(
    id: UUID, 
    session: SessionDep
) -> PaymentResponse:
    try: 
        return payment_service.read_payment_from_id(session, id)
    except PaymentNotFoundException: 
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Payment not found")

@router.get("/")
def get_payments(
    session: SessionDep
) -> List[PaymentResponse]:
    payments = payment_service.read_payments(session)
    return payments

@router.post("/", status_code=201)
async def create_payment(
    payment_request: PaymentCreateRequest,
    session: SessionDep
) -> PaymentResponse: 
    try: 
        payment = await payment_service.create_payment(
            session=session, 
            payment=payment_request
        )
        return payment
    except OrderNotFound:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Order not found")
    except UserNotFoundException:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Payment not found")


@router.patch("/{id}/confirm/")
async def confirm_payment(
    id,
    session: SessionDep
) -> PaymentResponse:
    try:
        new_status = PaymentUpdateRequest(status=PaymentStatusEnum.paid)
        return payment_service.update_payment(session=session, payment=new_status, payment_id=id)
    except PaymentNotFoundException:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Payment not found")
    
@router.patch("/{id}/cancel/")
async def confirm_payment(
    id: UUID,
    session: SessionDep
) -> PaymentResponse:
    try:
        new_status = PaymentUpdateRequest(status=PaymentStatusEnum.cancelled)
        return payment_service.update_payment(session=session, payment=new_status, payment_id=id)
    except PaymentNotFoundException:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Payment not found")
    
@router.get("/order/{order_id}/")
async def get_payments_from_order(
    order_id: UUID,
    session: SessionDep
):
    try:
        return payment_service.read_order_payments(session=session, order_id=order_id)
    except OrderNotFound:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Order not found")
    