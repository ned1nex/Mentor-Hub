import re
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from core.database import get_db
from .models import Request, RequestCreate, RequestPatch, RequestCreateResponse
from .repository import RequestRepository
from sqlalchemy.orm import Session

from uuid import UUID
from typing import List


router = APIRouter()


@router.post("/request", tags=["Request"], summary="Создание заявки.",
             responses={
                201: {"model": RequestCreateResponse, "description": "Заявка была успешно создана."},
                409: {"description": "Заявка уже была подана."},
             })
def make_request(
    request: RequestCreate,
    db: Session = Depends(get_db)
):
    request_repository = RequestRepository(db)

    if request_repository.get_request_by_pair(
        student_id=request.student_id,
        mentor_id=request.mentor_id
    ):
        return JSONResponse(
            status_code=409,
            content={"error": "already requested"}
        )
    
    request_id = request_repository.add_request(request)
    return JSONResponse(
        status_code=201,
        content=jsonable_encoder(
            RequestCreateResponse(request_id=request_id)
        )
    )



@router.get("/request/{request_id}", tags=["Request"], summary="Получение заявки по её ID.",
            responses={
                200: {"model": Request, "description": "Заявка успешно получена"},
                404: {"description": "Заявка не найдена."}
            })
def get_request_by_id(request_id: UUID, db: Session = Depends(get_db)):
    repository = RequestRepository(db)
    
    request = repository.get_request_by_request_id(request_id)
    if not request:
        return JSONResponse(
            status_code=404,
            content={"error": "not found"}
        )

    request_model = Request.model_validate(request.to_dict())
    
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(request_model)
    )


@router.get("/request/student/{student_id}", tags=["Request"], summary="Получение всех заявок по студента по его ID.",
            responses = {
                200: {"description": "Заявки были успешно получены.", "model": List[Request]},
                404: {"description": "Заявка не была найдена"}
            })
def get_requests_by_student_id(student_id: UUID, db: Session = Depends(get_db)):
    repository = RequestRepository(db)
    
    requests = repository.get_request_by_client_id(student_id)
    if not requests:
        return JSONResponse(
            status_code=404,
            content={"error": "not found"}
        )
    
    request_models: List[Request] = []
    for request in requests:
        request_model = Request.model_validate(request.to_dict())
        request_models.append(request_model)
    
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(request_models)
    )


@router.get("/request/mentor/{mentor_id}", tags=["Request"], summary="Получение всех заявок ментора",
            responses = {
                200: {"description": "Заявки были успешно получены.", "model": List[Request]},
                404: {"description": "Заявка не была найдена"}
            })
def get_requests_by_mentor_id(mentor_id: UUID, db: Session = Depends(get_db)):
    repository = RequestRepository(db)
    
    requests = repository.get_request_by_mentor_id(mentor_id)
    if not requests:
        return JSONResponse(
            status_code=404,
            content={"error": "not found"}
        )
    
    request_models: List[Request] = []
    for request in requests:
        request_model = Request.model_validate(request.to_dict())
        request_models.append(request_model)
    
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(request_models)
    )


@router.patch("/request/{request_id}",  tags=["Request"], summary="Изменение заявки",
            responses={
                200: {"description": "Заявка была успешно изменена.", "model": Request},
                404: {"description": "Заявка не была найдена"}
            })
def patch_request(
    request_id: UUID, 
    patch_model: RequestPatch,
    db: Session = Depends(get_db),
):
    repository = RequestRepository(db)

    request = repository.get_request_by_request_id(request_id)
    if not request:
        return JSONResponse(
            status_code=404,
            content={"error": "not found"}
        )
    
    patched_request = repository.patch_request(
        request_id=request_id,
        request_patch=patch_model
    )
    
    request_model = Request.model_validate(patched_request.to_dict())

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(request_model)
    )