from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from typing import Optional


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        authorization = request.headers.get("Authorization")
        
        if not authorization:
            raise HTTPException(
                status_code=401,
                detail="User not authorized",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (scheme and credentials) or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="User not authorized",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)



security = CustomHTTPBearer()
