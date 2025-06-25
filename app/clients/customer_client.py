import httpx
from app.core.settings import settings
from http import HTTPStatus
from uuid import UUID
import httpx
from app.exceptions import UserNotFoundException

class CustomerClient(): 
    async def get_user_by_id(self, customer_id: UUID):
        return {
            "name": "adne",
            "email": "qualquer",
            "password": "698dc19d489c4e4db73e28a713eab07b",
            "phone": "61995378511",
            "id": "42535e6f-ad2b-4032-acbf-8b237753da52",
            "created_at": "2025-06-25T15:15:37.134962",
            "updated_at": "2025-06-25T15:15:37.134977"
        } 
        async with httpx.AsyncClient() as client:   
            response = await client.get(settings.CUSTOMER_API + f"/customer/{customer_id}")
            if(response.status_code == HTTPStatus.NOT_FOUND):
                raise UserNotFoundException()
            return response.json()