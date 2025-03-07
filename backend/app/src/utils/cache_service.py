from typing import Optional, Dict, Any
from redis import Redis
import json


class CacheService:
    def __init__(self, cache: Redis):
        self.cache = cache

    def get_id_info(self, token: str) -> Optional[Dict[str, str]]:
        """Получение информации (id и handler) по токену"""
        result: bytes = self.cache.get(name=token)
        if not result:
            return None
        
        return json.loads(result.decode())
    
    def get_token_info(self, id: str) -> Optional[Dict[str, str]]:
        """Получение информации (token и handler) по id"""
        result: bytes = self.cache.get(id)
        if not result:
            return None
        
        return json.loads(result.decode())

    def set_id_with_handler(self, token: str, id: str, handler: str):
        """Установление token-id связи с указанием handler, где handler - это тип носителя ключа: student / mentor"""
        self.delete_id(token=token, id=id)

        token_data = {"id": id, "handler": handler}
        self.cache.setex(
            name=token, 
            value=json.dumps(token_data), 
            time=3600
        )
        
        id_data = {"token": token, "handler": handler}
        self.cache.setex(
            name=id, 
            value=json.dumps(id_data), 
            time=3600
        )

    def delete_id(self, token: Optional[str] = None, id: Optional[str] = None):
        """Удаление связи token-id"""
        if token:
            self.cache.delete(token)
        if id:
            self.cache.delete(id)
