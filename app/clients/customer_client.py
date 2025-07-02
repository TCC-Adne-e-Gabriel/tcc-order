import httpx
from app.core.settings import settings
from http import HTTPStatus
from uuid import UUID
import httpx
from app.exceptions import UserNotFoundException

class CustomerClient(): 
    async def fetch_user(self, customer_id: UUID):
        async with httpx.AsyncClient() as client:   
            response = await client.get(settings.CUSTOMER_API + f"/customer/{customer_id}")
            if(response.status_code == HTTPStatus.NOT_FOUND):
                raise UserNotFoundException()
            return response.json()