import httpx
from app.schemas.order import Product
from app.core.settings import settings
from http import HTTPStatus
from app.exceptions import ProductNotFoundException
from uuid import UUID
from app.schemas.order import UpdateQuantityRequest

class ProductClient(): 
    async def fetch_product(self, product_id: UUID, quantity: int) -> Product: 
        async with httpx.AsyncClient() as client:
            response = await client.get(
                settings.PRODUCT_API + f"/product/{product_id}/"
            )
            if(response.status_code == HTTPStatus.NOT_FOUND):
                raise ProductNotFoundException
            payload = UpdateQuantityRequest(quantity=quantity)
            await client.patch(
                url=settings.PRODUCT_API + f"/product/{product_id}/", 
                json=payload.model_dump()
            )
            return Product(**response.json())