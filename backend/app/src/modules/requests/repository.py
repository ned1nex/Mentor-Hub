from .schemas import Base, RequestORM
from sqlalchemy.orm import Session
from .models import Request, RequestPatch

from fastapi.encoders import jsonable_encoder
from typing import Optional
from uuid import UUID, uuid4


class RequestRepository():
    def __init__(self, db: Session) -> None:
        self.db = db
        Base.metadata.create_all(db.bind)

    def get_request_by_request_id(self, request_id: UUID):
        query = (
            self.db.query(RequestORM)
            .filter(RequestORM.request_id == request_id)
            .first()
        )
        return query

    def get_request_by_client_id(self, student_id: UUID):
        query = (
            self.db.query(RequestORM)
            .filter(RequestORM.student_id == student_id)
            .all()
        )
        return query
    
    def get_request_by_mentor_id(self, mentor_id: UUID):
        query = (
            self.db.query(RequestORM)
            .filter(RequestORM.mentor_id == mentor_id)
            .all()
        )
        return query
    
    def get_request_by_pair(self, student_id: UUID, mentor_id: UUID):
        query = (
            self.db.query(RequestORM)
            .filter(RequestORM.mentor_id == mentor_id)
            .filter(RequestORM.student_id == student_id)
            .first()
        )
        return query
    
    def add_request(self, request: Request) -> str:
        model_dict = jsonable_encoder(request.model_dump())

        request_id = str(uuid4())
        request_orm = RequestORM(
            request_id=request_id, 
            **model_dict
        )

        self.db.add(request_orm)
        self.db.commit()

        return request_id
    
    def patch_request(self, request_id: UUID, request_patch: RequestPatch) -> Optional[RequestORM]:
        changes = request_patch.model_dump(exclude_none=True)

        request = (
            self.db.query(RequestORM)
            .filter(RequestORM.request_id == str(request_id))
            .first()
        )

        if not request:
            return None
        
        for k, v in changes.items():
            setattr(request, k, v) # Меняем поля заявки

        self.db.commit()
        return request
    
    def get_all_requests(self):
        result = (
            self.db.query(RequestORM)
            .all()
        )
        return result