from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List
from uuid import UUID, uuid4
from app.core.encrypt import encrypt_data
from app.core.db import get_db_conn
from typing import Any
from datetime import datetime
from app.schemas.order import OrderCreateRequest, OrderStatusUpdate, OrderResponse, Message
from app.models.order import OrderStatusEnum
from app.deps import SessionDep
from app.services.order import OrderService
from exceptions import OrderNotFound
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
    conn=Depends(get_db_conn)
) -> OrderResponse:
    total_price = 0

    for item_data in order_request.products:
        if not isinstance(item_data, dict):
            raise HTTPException(status_code=400, detail="Product information is not as expected.")
        quantity = item_data.get("quantity")
        unit_price = item_data.get("unit_price")

        
        total_price += quantity * unit_price

    order_id = uuid4()
    date_now = datetime.now()
    cursor = conn.cursor()

    insert_order_query = """
        INSERT INTO orders (id, customer_id, freight, status, total_price, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    order_values = (
        str(order_id),
        str(customer_id),
        freight,
        'pending',
        total_price,
        date_now,
        date_now,
    )
    cursor.execute(insert_order_query, order_values)

    insert_order_product_query = """
        INSERT INTO order_product (order_id, product_id, quantity, unit_price)
        VALUES (%s, %s, %s, %s);
    """
    for item in products_list:
        order_product_values = (
            str(order_id),
            str(item["product_id"]),
            item["quantity"],
            item["unit_price"],
        )
        cursor.execute(insert_order_product_query, order_product_values)
    
    conn.commit() 
    body["id"] = order_id
    body["total_price"] = total_price
    body["created_at"] = date_now
    body["updated_at"] = date_now
    return {"order": body}


@router.patch("/{order_id}/")
async def update_order(
    order_id: UUID,
    order_data: Request,
    conn=Depends(get_db_conn)
):
    body = await order_data.json()
    cursor = conn.cursor()
    cursor.execute(
       f"SELECT id, customer_id, freight, total_price, created_at, updated_at, status FROM orders WHERE id = '{str(order_id)}'"
    )
    order_row = cursor.fetchone()

    if not order_row:
        raise HTTPException(status_code=404, detail="Order not found.")
    
    current_order_data = {
        "id": UUID(order_row[0]),
        "customer_id": UUID(order_row[1]),
        "freight": float(order_row[2]),
        "total_price": float(order_row[3]),
        "created_at": order_row[4],
        "updated_at": order_row[5],
        "status": OrderStatusEnum(order_row[6])
    }

    cursor.execute(
        "SELECT product_id, quantity, unit_price FROM order_product WHERE order_id = %s;",
        (str(order_id),)
    )
    current_products_data = [
        {"product_id": UUID(p[0]), "quantity": float(p[1]), "unit_price": float(p[2])}
        for p in cursor.fetchall()
    ]

    fields_to_update = []
    values_to_set = []
    
    new_updated_at = datetime.now()
    fields_to_update.append("updated_at = %s")
    values_to_set.append(new_updated_at)

    if "customer_id" in body:
        customer_id_str = body.get("customer_id")
        fields_to_update.append("customer_id = %s")
        values_to_set.append(customer_id_str)
        
    if "freight" in body:
        updated_freight = body.get("freight")
        fields_to_update.append("freight = %s")
        values_to_set.append(updated_freight)
        updated_products_list = current_products_data
    
    if "products" in body:
        products_val = body.get("products")
        updated_products_list = products_val

    parsed_products_for_total_calc = []
    response_order_products = []
    total_price = 0
    for item_data in updated_products_list: 
        product_id_str = item_data.get("product_id")
        quantity = item_data.get("quantity")
        unit_price = item_data.get("unit_price")

        product_id = UUID(product_id_str)
        
        parsed_products_for_total_calc.append({
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": unit_price
        })
        total_price += quantity * unit_price

    fields_to_update.append("total_price = %s")
    values_to_set.append(total_price)

    update_order_query = f"UPDATE orders SET {', '.join(fields_to_update)} WHERE id = %s;"
    values_to_set.append(str(order_id))

    cursor.execute(update_order_query, values_to_set)

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=400,
            detail="Order not found."
        )
    if "products" in body: 
        delete_order_products_query = f"DELETE FROM order_product WHERE order_id = '{order_id}';"
        cursor.execute(delete_order_products_query, (str(order_id),))
        insert_order_product_query = """
            INSERT INTO order_product (order_id, product_id, quantity, unit_price)
            VALUES (%s, %s, %s, %s);
        """
        for item in parsed_products_for_total_calc:
            order_product_values = (
                str(order_id),
                str(item["product_id"]),
                item["quantity"],
                item["unit_price"],
            )
            cursor.execute(insert_order_product_query, order_product_values)

    conn.commit()

    body["id"]=order_id,
    body["total_price"]=total_price,
    body["created_at"]=current_order_data["created_at"]
    body["updated_at"]=new_updated_at,
    body["status"]=current_order_data["status"],
    body["products"]=response_order_products
    
    return body
    
@router.delete("/{id}/")
def delete_order(
    id, 
    session: SessionDep
) -> Message:
    try: 
        order_service.delete_order(session=session, order_id=id)
    except OrderNotFound as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order not found")
    
    return Message(message="Order deleted successfully")

@router.patch("/{id}/status/")
def update_status(
    id,
    status_request: OrderStatusUpdate,
    session: SessionDep
) -> OrderResponse:
    try: 
        order = order_service.update_order_status(status_request)
    except OrderNotFound as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order not found")
    return order
    