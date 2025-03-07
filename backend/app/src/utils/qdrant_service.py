from typing import Dict, List, Any, Optional

from core.config import config

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

class QdrantService:
    def __init__(self):
        """Создаём кудрант"""
        self.client = QdrantClient(
            host=config.QDRANT_HOST, 
            port=config.QDRANT_PORT
        )
        self.collection_name = config.QDRANT_COLLECTION_NAME
        self.vector_size = config.QDRANT_VECTOR_SIZE
        
        # Ensure collection exists
        self._create_collection_if_not_exists()
        
    def _create_collection_if_not_exists(self):
        """Create the collection if it doesn't exist"""
        collections = self.client.get_collections().collections
        collection_names = [collection.name for collection in collections]
        
        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=qmodels.VectorParams(
                    size=self.vector_size,
                    distance=qmodels.Distance.COSINE
                )
            )

    
    def add_vector(self, vector: List[float], uuid_str: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        payload = metadata or {}

        payload["uuid"] = uuid_str
        
        operation_result = self.client.upsert(
            collection_name=self.collection_name,
            points=[
                qmodels.PointStruct(
                    id=uuid_str,
                    vector=vector,
                    payload=payload
                )
            ]
        )
        
        return operation_result.status == qmodels.UpdateStatus.COMPLETED
    
    def delete_vector(self, uuid_str: str) -> bool:
        operation_result = self.client.delete(
            collection_name=self.collection_name,
            points_selector=qmodels.PointIdsList(
                points=[uuid_str]
            )
        )
        
        return operation_result.status == qmodels.UpdateStatus.COMPLETED
    
    def find_similar_vectors(self, query_vector: List[float], limit: int = 10, score_threshold: float = 0.5) -> List[Dict[str, Any]]:
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold
        )
        
        results = []
        for scored_point in search_result:
            # Extract the payload and add the score
            result_dict = scored_point.payload.copy() if scored_point.payload else {"uuid": None}
            result_dict["score"] = scored_point.score
            results.append(result_dict)
            
        return results

    def count_points(self) -> int:
        """Get the number of points in the collection"""
        return self.client.count(collection_name=self.collection_name).count
