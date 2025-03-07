from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from uuid import UUID
from redis import Redis
from sqlalchemy.orm import Session

from common.dependencies import (
    get_student_service,
    get_mentor_service
)
from core.database import get_db
from core.cache import get_cache
from .service import StatisticsService
from .models import AdminStats, MentorStats

router = APIRouter()

@router.get("/stats/{mentor_id}", summary="Получение статистики по ментору.", tags=["Stats"],
            responses={
                200: {"model": MentorStats, "description": "Статистика была успешно получена"},
                404: {"description": "Статистика не была найдена."}
            })
def get_mentor_stats(
    mentor_id: UUID, 
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    stat_service = StatisticsService(db, cache)
    mentor_service = get_mentor_service(db, cache)
    stats = stat_service.get_mentor_statistics(mentor_id)

    mentor = mentor_service.get_mentor_by_id(mentor_id)
    if not mentor:
        return JSONResponse(
            status_code=404,
            content={"error": "not found"}
        )

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(stats)
    )


@router.get("/stats", summary="Получение статистики по всему серверу", tags=["Stats"],
            responses={
                200: {"model": AdminStats, "description": "Статистика была успешно получена"},
                404: {"description": "Статистика не была найдена."}
            })
def get_stats(
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    stat_service = StatisticsService(db, cache)
    stats = stat_service.get_administrator_stats()

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(stats)
    )