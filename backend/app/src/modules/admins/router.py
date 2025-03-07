# Вспомогательный роутер

from uuid import UUID
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends
from redis import Redis

from sqlalchemy.orm import Session

from core.cache import get_cache
from core.database import get_db
from common.auth.dependencies import get_token
from common.dependencies import (
    get_cache_service,
    get_password_token_service
)

from .service import AdminRepositoryService
from .repository import AdminRepository
from .models import AdminCreate, Admin, AdminRegisterStatus

router = APIRouter()

@router.post(
        "/admin/sign-up", 
        summary="Регистрация админа", 
        tags=["Admin"],
        responses={
            201: {"model": AdminRegisterStatus, "description": "Успешная регистрация админа"},
            422: {"description": "Ошибка валидации"}
        })
def register_admin(
    admin_register: AdminCreate,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    repository = AdminRepository(db)
    password_service = get_password_token_service()
    cache_service = get_cache_service(cache)

    # Хешируем пароль
    password = admin_register.password
    hashed_password = password_service.hash_password(password)
    admin_register.password = hashed_password

    # Устанавливаем токен
    status = repository.add_admin(admin_register)
    status.token = password_service.generate_token(str(status.id))

    # Устанавливаем связь в кеше
    cache_service.set_id_with_handler(status.token, str(status.id), "admin")
    
    return JSONResponse(
        status_code=201,
        content=jsonable_encoder(status)
    )


@router.post("/admin/sign-in", summary="Регистрация админа", tags=["Admin"],
        responses={
            200: {"model": AdminRegisterStatus, "description": "Успешная регистрация админа"},
            404: {"description": "Админ не найден"},
            403: {"description": "Неверные данные для входа"},
            422: {"description": "Ошибка валидации"}
        })
def login_admin(
    admin_login: AdminCreate,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    repository = AdminRepository(db)
    service_repo = AdminRepositoryService(db, cache)

    admin = repository.get_admin_by_email(admin_login.email)

    if not admin:
        return JSONResponse(
            status_code=404,
            content={"error": "not found"}
        )
    
    status = service_repo.admin_login(
        admin_login.email,
        admin_login.password
    )

    if not status:
        return JSONResponse(
            status_code=403,
            content={"status": "wrong credentials"}
        )

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(status)
    )