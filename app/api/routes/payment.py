from fastapi import FastAPI, Depends, APIRouter, HTTPException
from app.services.payment_mock import PaymentMockService
from uuid import UUID
from typing import List
from app.services.payment import PaymentService
from app.schemas.payment import PaymentResponse, PaymentCreateRequest, PaymentUpdateRequest
from app.models.payment import PaymentStatusEnum
from app.deps import SessionDep
from app import auth
from app.schemas.auth import TokenData
from app.context import user_id_context


app = FastAPI()
router = APIRouter(prefix="/payment")
payment_mock = PaymentMockService()
payment_service = PaymentService()

@router.get("/{id}/", response_model=PaymentResponse)
def get_payment_by_id(
    id: UUID, 
    session: SessionDep, 
    decoded_token = Depends(auth.role_required(["admin"]))
):
    user_id_context.set(decoded_token.id)
    return payment_service.read_payment_from_id(session, id)


@router.get("/", response_model=List[PaymentResponse])
def get_payments(
    session: SessionDep, 
    decoded_token = Depends(auth.role_required(["admin"]))
):
    user_id_context.set(decoded_token.id)
    payments = payment_service.read_payments(session)
    return payments


@router.post("/", status_code=201, response_model=PaymentResponse)
async def create_payment(
    payment_request: PaymentCreateRequest,
    session: SessionDep,
    decoded_token: TokenData = Depends(auth.role_required(["user"]))
): 
    user_id_context.set(decoded_token.id)
    payment = await payment_service.create_payment(
        session=session, 
        payment=payment_request, 
        customer_id=decoded_token.id
    )
    return payment


@router.patch("/{id}/confirm/", response_model=PaymentResponse)
async def confirm_payment(
    id,
    session: SessionDep, 
    decoded_token = Depends(auth.role_required(["service", "admin"]))
):
    user_id_context.set(decoded_token.id)
    new_status = PaymentUpdateRequest(status=PaymentStatusEnum.paid)
    return payment_service.update_payment(session=session, payment=new_status, payment_id=id)


@router.patch("/{id}/cancel/", response_model=PaymentResponse)
async def confirm_payment(
    id: UUID,
    session: SessionDep, 
    decoded_token = Depends(auth.role_required(["service", "admin"]))
):
    user_id_context.set(decoded_token.id)
    new_status = PaymentUpdateRequest(status=PaymentStatusEnum.cancelled)
    return payment_service.update_payment(session=session, payment=new_status, payment_id=id)


@router.get("/order/{order_id}/", response_model=List[PaymentResponse])
async def get_payments_from_order(
    order_id: UUID,
    session: SessionDep, 
    decoded_token = Depends(auth.role_required(["service", "admin"]))
):
    user_id_context.set(decoded_token.id)
    return payment_service.read_order_payments(session=session, order_id=order_id)
    