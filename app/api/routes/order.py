from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List
from uuid import UUID, uuid4
from datetime import datetime
from app.schemas.order import OrderCreateRequest, OrderStatusUpdate, OrderResponse, Message, OrderUpdateRequest
from app.deps import SessionDep
from app.services.order import OrderService
from app.exceptions import OrderNotFound, ProductNotFoundException
from http import HTTPStatus


app = FastAPI()
router = APIRouter(prefix="/order")
order_service = OrderService()

@router.get("/{id}/")
def get_order_by_id(
    id: UUID, 
    session: SessionDep
) -> OrderResponse:
    try: 
        order = order_service.get_order_by_id(session=session, order_id=id)
    except OrderNotFound as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order not found")
    return order


@router.get("/")
def get_orders(
    session: SessionDep
) -> List[OrderResponse]:
    orders = order_service.get_orders(session)
    return orders


@router.post("/", status_code=201)
async def create_order(
    order_request: OrderCreateRequest,
    session: SessionDep
) -> OrderResponse:
    try: 
        order = await order_service.create_order(session, order_request)
        return order
    except ProductNotFoundException as e: 
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
    except OrderNotFound as e: 
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order not found")

    
@router.delete("/{id}/")
def delete_order(
    id, 
    session: SessionDep
) -> Message:
    try: 
        order_service.delete_order(session=session, order_id=id)
        return Message(message="Order deleted successfully")
    except OrderNotFound as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order not found")
    

@router.patch("/{id}/status/")
def update_status(
    id,
    status_request: OrderStatusUpdate,
    session: SessionDep
) -> OrderResponse:
    try: 
        order = order_service.update_order_status(session=session, status_update=status_request, order_id=id)
        return order
    except OrderNotFound as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order not found")
    