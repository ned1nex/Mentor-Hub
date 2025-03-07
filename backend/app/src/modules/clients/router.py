# FastAPI Router

from uuid import UUID
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from typing import Annotated

from common.dependencies import (
    get_cache_service,
    get_password_token_service
)

from .service import StudentRepositoryService
from .repository import StudentRepository
from .models import  Student, StudentCreate, StudentSignIn, StudentPatch, StudentRegisterStatus

from fastapi import Depends
from sqlalchemy.orm import Session
from redis import Redis

from core.database import get_db
from core.cache import get_cache
from common.auth.dependencies import get_token

router = APIRouter()

@router.post("/students/sign-up", summary="регистрация пользователя", tags=["Student"],
        responses={
            201: {"model": StudentRegisterStatus, "description": "Успешная регистрация студента"},
            409: {"description": "Студент уже был зарегистрирован"}
        }, status_code=201)
def student_sign_up(
    student_create: StudentCreate,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    repository = StudentRepository(db, cache)
    cache_service = get_cache_service(cache)
    password_service = get_password_token_service()

    if repository.get_student_by_email(student_create.email):
        return JSONResponse(
            status_code=409,
            content={"detail": "already exists"}
        )
    
    # Хешируем пароль
    password = student_create.password
    hashed_password = password_service.hash_password(password)
    student_create.password = hashed_password

    # Добавляет студента в бд
    status = repository.add_student(student_create)
    token = password_service.generate_token(status.id)
    
    # Обновляем в кеше токен (носитель токена: handler)
    cache_service.set_id_with_handler(token, status.id, handler="student")

    # Обновляем в статусе токен
    status.token = token

    return JSONResponse(
        status_code=201,
        content=jsonable_encoder(status)
    )

@router.post("/students/sign-in", tags=["Student"], summary="вход в аккаунт студента",
        responses={
            200: {"model": StudentRegisterStatus, "description": "Успешная регистрация студента"},
            404: {"description": "Студент не найден"},
            403: {"description": "Пользователь не авторизован"},
        })
def student_sign_in(
    student_create: StudentSignIn,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    repository = StudentRepository(db, cache)
    service_repo = StudentRepositoryService(db, cache)

    # Получаем студента из базы
    student = repository.get_student_by_email(student_create.email)
    if not student:
        return JSONResponse(
            status_code=404, 
            content={"error": "student not found"}
        )
    
    # Проверяем аутентификацию
    status = service_repo.student_login(student_create.email, student_create.password)
    if not status.status:
        return JSONResponse(
            status_code=403, 
            content={"error": "not authenticated"}
        )

    # Используем Pydantic `.model_dump()`, который уже преобразует UUID в строку
    return JSONResponse(
        status_code=200, 
        content=jsonable_encoder(status)
    )



@router.patch("/students/{student_id}", tags=["Student"], summary="Обновление данных студента",
        responses={
            200: {"model": Student, "description": "Студент обновлён"},
            404: {"description": "Студент не найден"},
        })
def patch_student(
    student_id: UUID,
    patch_model: StudentPatch,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    repository = StudentRepository(db, cache)

    student = repository.get_student_by_id(student_id)
    if not student:
        return JSONResponse(
            status_code=404,
            content={"error": "student not found"}
        )

    updated_student = repository.patch_student(student_id, patch_model)
    student_model = Student.model_validate(updated_student.to_dict())

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(student_model)
    )


@router.get("/students", tags=["Student"], summary="Получение студента по токену.",
        responses={
            200: {"model": Student, "description": "Студент успешно получен"},
            404: {"description": "Студент не найден"},
        })
def get_student(
    token: Annotated[str, Depends(get_token)],
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    repository = StudentRepository(db, cache)
    cache_service = get_cache_service(cache)

    student_id = cache_service.get_id_info(token)
    if not student_id:
        return JSONResponse(
            status_code=404,
            content={"error": "not found"}
        )

    student = repository.get_student_by_id(student_id.get("id", ""))
    student_model = Student.model_validate(student.to_dict())

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(student_model)
    )


@router.get("/students/{student_id}", summary="Получение студента по ID", tags=["Student"])
def get_student_by_id(student_id: UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    repository = StudentRepository(db, cache)

    student = repository.get_student_by_id(student_id)
    if not student:
        return JSONResponse(
            status_code=404,
            content={"error": "client not found"}
        )

    return jsonable_encoder(student)