# Общие зависимости

from redis import Redis
from sqlalchemy.orm import Session

from src.utils.qdrant_service import QdrantService
from src.utils.password_service import PasswordTokenService
from src.utils.cache_service import CacheService
from src.utils.model_service import VectorService

# Сервисы модулей
from src.modules.requests.service import RequestRepositoryService
from src.modules.mentors.repository_services.service import MentorRepositoryService
from src.modules.clients.repository_services.service import StudentRepositoryService

def get_password_token_service():
    return PasswordTokenService()


def get_cache_service(cache: Redis):
    return CacheService(cache=cache)


def get_qdrant_service():
    return QdrantService()


def get_vectorise_service():
    return VectorService()


def get_request_service(db: Session):
    return RequestRepositoryService(db)


def get_mentor_service(db: Session, cache: Redis):
    return MentorRepositoryService(db, cache)   


def get_student_service(db: Session, cache: Redis):
    return StudentRepositoryService(db, cache)