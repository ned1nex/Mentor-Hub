# FastAPI Router

from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Body, Query
from fastapi import Depends
from fastapi import BackgroundTasks
from sqlalchemy import JSON

from core.database import get_db
from core.cache import get_cache

from common.dependencies import (
    get_cache_service,
    get_password_token_service
)
from .service import MentorRepositoryService, MentorQdrantService
from .repository import MentorRepository
from .models import MentorRegister, MentorRegisterStatus, MentorSearchResponse, MentorSignIn, Mentor

from redis import Redis
from typing import Dict, List, Tuple
from sqlalchemy.orm import Session
from uuid import UUID, uuid4

router = APIRouter()

@router.get("/mentors/{mentor_id}", tags=["Mentor"], summary="Получение ментора по ID.",
            responses={
                200: {"model": Mentor, "description": "Ментор успешно получен"},
                404: {"description": "Ментор не найден"}
                }
            )
def get_mentor_by_id(
        mentor_id: UUID,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_cache)
):
    repository = MentorRepository(db, cache)
    mentor = repository.get_mentor_by_id(mentor_id)

    if not mentor:
        return JSONResponse(
            content={},
            status_code=404
        )

    mentor_model = Mentor.model_validate(mentor.to_dict())

    return JSONResponse(
        content=jsonable_encoder(mentor_model),
        status_code=200
    )


@router.get("/mentors", tags=["Mentor"], summary="Поиск менторов по запросу.",
        responses={
            200: {"model": List[MentorSearchResponse], "description": "Список менторов по запросу получен"},
            })
def get_mentors(
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache),
    query: str = Query(min_length=1),
):
    repository = MentorRepository(db, cache)
    qdrant_service = MentorQdrantService()

    mentors = qdrant_service.get_qdrant_mentors(query, threshold=0)

    mentor_models: List[Dict] = []
    for mentor in mentors:
        id, score = mentor

        mentor = repository.get_mentor_by_id(id)
        if not mentor:
            continue

        mentor_models.append(
            {
                "mentor": Mentor.model_validate(mentor.to_dict()),
                "score": score,
            }
            
        )

    return JSONResponse(
        content=jsonable_encoder(mentor_models),
        status_code=200
    )


@router.post("/mentors/{mentor_id}/score", tags=["Mentor"], summary="Изменение рейтинга ментора.",
        responses={
            404: {"description": "Ментор не найден"},
            200: {"model": Mentor, "description": "Скор ментора успешно изменен"}
        })
def add_score(
    mentor_id: UUID,
    score: int = Body(..., embed=True, ge=0, le=10),
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    repository = MentorRepository(db, cache)

    mentor = repository.get_mentor_by_id(mentor_id)
    if not mentor:
        return JSONResponse(
            status_code=404,
            content={"error": "not found"}
        )
    
    updated = repository.add_score(
        str(mentor_id), score
    )
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(updated)
    )



@router.post("/mentors/sign-up", tags=["Mentor"], summary="Регистрация ментора.",
        responses={
            201: {"model": MentorRegisterStatus, "description": "Ментор успешно зарегистрирован."},
            409: {"description": "Ментор уже был зарегистрирован"}
        }
    )
def sign_up_mentor(
    mentor_register: MentorRegister,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache),
):
    repository = MentorRepository(db, cache)
    qdrant_service = MentorQdrantService()
    password_service = get_password_token_service()
    cache_service = get_cache_service(cache)

    if repository.get_mentor_by_email(mentor_register.email):
        return JSONResponse(
            status_code=409,
            content={"error": "mentor already registered"}
        )

    # Add mentor to the database first
    password = mentor_register.password
    hashed_password = password_service.hash_password(password)
    mentor_register.password = hashed_password

    # Добавляем ментора в репозиторий
    status = repository.add_mentor(mentor_register)

    # Генерируем токен
    token = password_service.generate_token(str(status.id))
    status.token = token

    # Обновляем в редисе
    cache_service.set_id_with_handler(token, str(status.id), "mentor")

    # Move the Qdrant operation to a background task
    background_tasks.add_task(
        qdrant_service.add_qdrant_mentor,
        mentor_id=str(status.id),
        mentor=mentor_register,
    )

    return JSONResponse(
        status_code=201,
        content=jsonable_encoder(status)
    )


@router.post("/mentors/sign-in", tags=["Mentor"], summary="Вход ментора.",
        responses={
            201: {"model": MentorRegisterStatus, "description": "Ментор успешно залогинился."},
            403: {"description": "Неверные учётные данные"},
            404: {"description": "Ментор не найден."}
        })
def sign_in_mentor(
    mentor_sign_in: MentorSignIn,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    repository = MentorRepository(db, cache)
    service_repo = MentorRepositoryService(db, cache)

    mentor = repository.get_mentor_by_email(mentor_sign_in.email)

    if not mentor:
        return JSONResponse(
            status_code=404,
            content={"error": "not found"}
        )

    # Авторизация
    status = service_repo.mentor_login(
        mentor_email=mentor_sign_in.email,
        mentor_password=mentor_sign_in.password
    )

    if not status.status:
        return JSONResponse(
            status_code=403,
            content={"status": "wrong credentials"}
        )
    
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(status)
    )