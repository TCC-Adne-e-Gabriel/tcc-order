from fastapi import FastAPI
from fastapi import APIRouter, HTTPException
from app.services.payment_mock import PaymentMockService
from uuid import UUID, uuid4
from typing import List
from app.services.payment import PaymentService
from app.exceptions import PaymentNotFoundException
from app.schemas.payment import PaymentResponse
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
        payment_service.get_payment_from_id(session, id)
    except PaymentNotFoundException as e: 
        raise HTTPException(HTTPStatus.NOT_FOUND)

@router.get("/")
def get_payments(
    session: SessionDep
) -> List[PaymentResponse]:
    payments = payment_service.get_payments(session)
    return payments

# @router.post("/", status_code=201)
# async def create_payment(
#     request: Request,
#     conn=Depends(get_db_conn)
# ) -> Any: 
    
#     body = await request.json()
#     cursor = conn.cursor()
#     payment_id = uuid4()
#     date_now = datetime.now()
#     status = payment_mock.mock_payment(body["payment_method"])

#     query = """
#         INSERT INTO payment (id, created_at, updated_at, payment_method, status, order_id, paid_at, customer_id, number_of_installments, total_amount)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
#     """
#     values = (
#         str(payment_id),
#         date_now,
#         date_now,
#         body["payment_method"], 
#         status,
#         str(body["order_id"]),
#         (date_now if status == PaymentStatusEnum.paid else None),
#         str(body["customer_id"]),
#         body["number_of_installments"], 
#         body["total_amount"]
#     )
            
#     body["id"] = payment_id
#     body["created_at"] = date_now
#     body["updated_at"] = date_now
#     body["paid_at"] = date_now if status == PaymentStatusEnum.paid else None
#     body["status"] = status
#     if body["payment_method"] == PaymentMethodEnum.boleto:
#         body["barcode"] = payment_mock.mock_barcode()
#     cursor.execute(query, values)
#     conn.commit()
#     cursor.close()
#     return body

# @router.patch("/{id}/confirm/")
# async def confirm_payment(
#     id,
#     password_request: Request,
#     conn=Depends(get_db_conn),     
# ):
#     password_request = await password_request.json()
#     cursor = conn.cursor()
#     cursor.execute(f"UPDATE payment SET status ='{PaymentStatusEnum.paid}' WHERE id = '{id}'")
#     conn.commit()
#     cursor.close()
#     if cursor.rowcount == 0:
#         cursor.close()
#         raise HTTPException(status_code=404, detail="Payment not found")
    
#     return { "message": "Payment paid successfully"}

# @router.patch("/{id}/cancel/")
# async def cancel_payment(
#     id,
#     password_request: Request,
#     conn=Depends(get_db_conn),     
# ):
#     password_request = await password_request.json()
#     cursor = conn.cursor()
#     cursor.execute(f"UPDATE payment SET status ='{PaymentStatusEnum.cancelled}' WHERE id = '{id}'")
#     conn.commit()
#     cursor.close()
#     if cursor.rowcount == 0:
#         cursor.close()
#         raise HTTPException(status_code=404, detail="Payment not found")
    
#     return { "message": "Payment cancelled successfully"}