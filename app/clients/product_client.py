import requests
from app.core.settings import settings
from http import HTTPStatus
from exceptions import UserNotFoundException
from uuid import UUID, uuid4

class ProductClient(): 
    async def get_user_by_id(self, product_id: UUID): 
        response = await requests.get(settings.CUSTOMER_API + f"/product/{product_id}")
        if(response.status_code == HTTPStatus.NOT_FOUND):
            raise UserNotFoundException()
        return response.content