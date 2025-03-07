# Вспомогательный роутер

from uuid import UUID
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRouter
from fastapi import Depends
from redis import Redis

from core.cache import get_cache
from common.auth.dependencies import get_token
from common.dependencies import get_cache_service

from .service import CalendarGeneratorService
from .models import RoleResponse, CalendarModel, CalendarResponse

router = APIRouter()

@router.get("/get-role/{instance_id}", summary="Получение роли (ментор/студент) по его ID", tags=["Support"],
            responses = {
                200: {"model": RoleResponse, "description": "Роль была успешно получена"},
                404: {"description": "Роль не найдена (объект не существует или не был зарегистрирован)"}
            })
def get_role_by_id(
    instance_id: UUID,
    cache: Redis = Depends(get_cache)
):
    cache_service = get_cache_service(cache)

    instance = cache_service.get_token_info(str(instance_id))
    if not instance:
        return JSONResponse(
            status_code=404,
            content={"error": "not found"}
        )
    
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(
            RoleResponse(
                role=instance.get("handler"),
                id=instance.get("id", "")
            )
        )
    )



@router.get("/get-role", summary="Получение роли (ментор/студент) по его Токену", tags=["Support"],
            responses = {
                200: {"model": RoleResponse, "description": "Роль была успешно получена"},
                404: {"description": "Роль не была найдена (объект не зарегистрирован)"}
            })
def get_role_by_token(
    token: str = Depends(get_token),
    cache: Redis = Depends(get_cache)
):
    cache_service = get_cache_service(cache)

    instance = cache_service.get_id_info(str(token))
    if not instance:
        return JSONResponse(
            status_code=404,
            content={"error": "not found"}
        )
    
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(
            RoleResponse(
                role=instance.get("handler"),
                id=instance.get("id", "")
            )
        )
    )


@router.post("/calendar", summary="Получение файла с календарём", tags=["Support"],
             responses={
                 422: {"description": "Ошибка валидации, неверная дата"},
                 200: {"model": CalendarResponse, "description": "Календарь успешно сгенерирован"}
             })
def get_calendar(calendar_model: CalendarModel):
    service = CalendarGeneratorService()

    if not service.is_valid_date(calendar_model.date):
        return JSONResponse(
            status_code=422,
            content={"error": "date is invalid"}
        )
    
    calendar_file: bytes = service.generate_calendar_file(calendar_model.date)
    
    filename = f"event_{calendar_model.date}.ics"
    return Response(
        content=calendar_file,
        media_type="text/calendar",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "text/calendar; charset=utf-8",
        },
        status_code=200
    )
