import httpx
from app.schemas.order import Product
from app.core.settings import settings
from http import HTTPStatus
from app.exceptions import ProductNotFoundException
from uuid import UUID
from app.schemas.order import UpdateQuantityRequest

class ProductClient(): 
    async def get_product_by_id(self, product_id: UUID, quantity: int) -> Product: 
        return Product(**{
            "name": "Camisa Básica Masculina",
            "description": "Camisa de algodão confortável, ideal para o dia a dia.",
            "price": 49.9,
            "sku": "CAMISABASICA123",
            "quantity": 100,
            "available": True,
            "image": None,
            "id": "8d99a0d5-0ec7-4235-807a-f1bfd48f0d5a",
            "created_at": "2025-06-25T15:54:35.646925",
            "updated_at": "2025-06-25T15:54:35.646942",
            "categories": []
        })
        async with httpx.AsyncClient() as client:
            response = await client.get(
                settings.PRODUCT_API + f"/product/{product_id}"
            )
            if(response.status_code == HTTPStatus.NOT_FOUND):
                raise ProductNotFoundException()
            payload = UpdateQuantityRequest(quantity=quantity)
            await client.patch(
                url=settings.PRODUCT_API + f"/product/{product_id}", 
                json=payload.model_dump()
            )
            return Product(**response.json())