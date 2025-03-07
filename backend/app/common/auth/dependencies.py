from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from typing import Annotated

from core.cache import get_cache
from ..dependencies import get_cache_service
from .security import security


def get_token(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        cache = Depends(get_cache)
    ):
    token = credentials.credentials

    cache_service = get_cache_service(cache)
    result = cache_service.get_id_info(token)

    # Ошибка авторизации
    if not result:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
        
    return token