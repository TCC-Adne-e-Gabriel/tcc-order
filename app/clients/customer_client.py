import requests
from app.core.settings import settings
from http import HTTPStatus
from exceptions import UserNotFoundException

class CustomerClient(): 
    async def get_user_by_id(self, customer_id: str): 
        response = await requests.get(settings.CUSTOMER_API + f"/customer/{customer_id}")
        if(response.status_code == HTTPStatus.NOT_FOUND):
            raise UserNotFoundException()
        return response.content