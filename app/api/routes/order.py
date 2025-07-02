from fastapi import FastAPI, APIRouter, Depends
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
from app.services.payment import PaymentService
from app import auth
from app.schemas.auth import TokenData

app = FastAPI()
router = APIRouter(prefix="/order")
order_service = OrderService()
payment_service = PaymentService()


@router.get("/{id}/", response_model=OrderResponse, dependencies=[Depends(auth.role_required(["admin", "user"]))])
async def get_order_by_id(
    id: UUID, 
    session: SessionDep
) -> OrderResponse:
    order = await order_service.read_order_by_id(session=session, order_id=id)
    return order

@router.get("/{id}/payments", response_model=OrderResponse, dependencies=[Depends(auth.role_required(["admin", "user"]))])
def get_order_payments(
    id: UUID, 
    session: SessionDep
):
    order = payment_service.read_payments_from_order(
        session=session, 
        order_id=id
    )
    return order

@router.get("/", response_model=List[OrderResponse], dependencies=[Depends(auth.role_required(["admin"]))])
async def get_orders(
    session: SessionDep
):
    orders = await order_service.read_orders(session)
    return orders

@router.get("/customer/{id}", response_model=List[OrderResponse], dependencies=[Depends(auth.role_required(["admin"]))])
async def get_orders_customer(
    id: UUID,
    session: SessionDep
) -> List[OrderResponse]:
    orders = await order_service.read_orders_from_customer(session=session, customer_id=id)
    return orders

@router.get("/me/", response_model=List[OrderResponse])
async def get_orders_current_customer(
    session: SessionDep,
    token_data: TokenData = Depends(auth.role_required(["admin", "user"]))
) -> List[OrderResponse]:
    orders = await order_service.read_orders_from_customer(session=session, customer_id=token_data.id)
    return orders

@router.post("/", status_code=201, response_model=OrderResponse)
async def create_order(
    order_request: OrderCreateRequest,
    session: SessionDep, 
    token_data: TokenData = Depends(auth.role_required(["admin", "user"]))
) -> OrderResponse:
    order = await order_service.create_order(session, order_request, token_data.id)
    return order

@router.patch("/{order_id}/", response_model=OrderResponse, dependencies=[Depends(auth.role_required(["user", "admin"]))])
async def update_order(
    order_id: UUID,
    order_data: OrderUpdateRequest,
    session: SessionDep
) -> OrderResponse:
    order = await order_service.update_order(session=session, order=order_data, order_id=order_id)
    return order

@router.patch("/{id}/status/", response_model=OrderSimpleResponse, dependencies=[Depends(auth.role_required(["admin"]))])
def update_status(
    id,
    status_request: OrderStatusUpdate,
    session: SessionDep
) -> OrderSimpleResponse:
    order = order_service.update_order_status(session=session, status_update=status_request, order_id=id)
    return order
    
@router.delete("/{id}/", response_model=Message, dependencies=[Depends(auth.role_required(["admin"]))])
def delete_order(
    id, 
    session: SessionDep
):
    order_service.delete_order(session=session, order_id=id)
    return Message(message="Order deleted successfully")
