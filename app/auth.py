from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.exceptions import (
    InvalidPasswordException, 
    UnauthorizedException,
)
from http import HTTPStatus
import jwt
from jwt import InvalidTokenError
from app.core.settings import Settings
from typing import List
from app.clients.customer_client import CustomerClient
from app.schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
settings = Settings()
customer_client = CustomerClient()

        
async def get_current_customer_role(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        customer_id = payload.get("sub")
        role = payload.get("role")
        if customer_id is None:
            raise InvalidTokenError
        if role is None: 
            raise InvalidTokenError
        token_data = TokenData(id=customer_id, role=role)
    except InvalidTokenError:
        raise InvalidPasswordException(HTTPStatus.BAD_REQUEST, detail="Invalid Credentials")
    return token_data

def role_required(roles: List[str]):
    async def checker(decoded_token: TokenData = Depends(get_current_customer_role)):
        if not decoded_token.role in roles:
            raise UnauthorizedException(HTTPStatus.UNAUTHORIZED, detail="User unauthorized")
        return decoded_token
    return checker