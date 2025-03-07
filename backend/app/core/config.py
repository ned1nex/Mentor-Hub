# Здесь config

from pydantic_settings import BaseSettings

class Config(BaseSettings):
    PORT: int
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    REDIS_HOST: str
    REDIS_PORT: int
    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_COLLECTION_NAME: str
    QDRANT_VECTOR_SIZE: int
    OLLAMA_HOST: str
    OLLAMA_PORT: int

    class Config:
        env_file = ".env"  # Указываем, откуда брать переменные

config = Config()