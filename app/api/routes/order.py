from fastapi import FastAPI
from fastapi import APIRouter, HTTPException
from typing import List
from uuid import UUID
from app.schemas.order import (
    OrderCreateRequest, 
    OrderStatusUpdate, 
    OrderResponse, 
    Message, 
    OrderUpdateRequest, 
    OrderSimpleResponse
)
from app.deps import SessionDep
from app.services.order import OrderService
from app.exceptions import OrderNotFound, ProductNotFoundException, UserNotFoundException
from http import HTTPStatus
from app.services.payment import PaymentService


app = FastAPI()
router = APIRouter(prefix="/order")
order_service = OrderService()
payment_service = PaymentService()

@router.get("/{id}/")
async def get_order_by_id(
    id: UUID, 
    session: SessionDep
) -> OrderResponse:
    try: 
        order = await order_service.read_order_by_id(session=session, order_id=id)
    except OrderNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order not found")
    return order

@router.get("/{id}/payments")
def get_order_payments(
    id: UUID, 
    session: SessionDep
) -> OrderResponse:
    try: 
        order = payment_service.read_payments_from_order(
            session=session, 
            order_id=id
        )
    except OrderNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order not found")
    return order

@router.get("/")
async def get_orders(
    session: SessionDep
) -> List[OrderResponse]:
    orders = await order_service.read_orders(session)
    return orders

@router.get("/me/{id}")
async def get_orders_customer(
    id: UUID,
    session: SessionDep
) -> List[OrderResponse]:
    try:
        orders = await order_service.read_orders_from_customer(session=session, customer_id=id)
        return orders
    except UserNotFoundException: 
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

@router.post("/", status_code=201)
async def create_order(
    order_request: OrderCreateRequest,
    session: SessionDep
) -> OrderResponse:
    try: 
        order = await order_service.create_order(session, order_request)
        return order
    except ProductNotFoundException: 
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Product not found")

@router.patch("/{order_id}/")
async def update_order(
    order_id: UUID,
    order_data: OrderUpdateRequest,
    session: SessionDep
) -> OrderResponse:
    try: 
        order = await order_service.update_order(session=session, order=order_data, order_id=order_id)
        return order
    except OrderNotFound: 
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order not found")

@router.patch("/{id}/status/")
def update_status(
    id,
    status_request: OrderStatusUpdate,
    session: SessionDep
) -> OrderSimpleResponse:
    try: 
        order = order_service.update_order_status(session=session, status_update=status_request, order_id=id)
        return order
    except OrderNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order not found")
    
@router.delete("/{id}/")
def delete_order(
    id, 
    session: SessionDep
) -> Message:
    try: 
        order_service.delete_order(session=session, order_id=id)
        return Message(message="Order deleted successfully")
    except OrderNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order not found")