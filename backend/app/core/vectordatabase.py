# Здесь yield векторной базы данных

from qdrant_client import QdrantClient
from config import config

qdrant_client = QdrantClient(
    host=config.QDRANT_HOST,
    port=config.QDRANT_PORT,
)

def get_qdrant_db() -> QdrantClient:
    return qdrant_client
