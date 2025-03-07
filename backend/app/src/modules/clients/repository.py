from typing import List, Optional, Dict, Type
from uuid import UUID, uuid4

from redis import Redis
from sqlalchemy.orm import Session

from .models import Student, StudentCreate, StudentRegisterStatus, StudentPatch
from .schemas import Base, StudentORM

class StudentRepository:
    def __init__(
            self, 
            db: Session, 
            cache: Redis):
        self.db = db
        Base.metadata.create_all(db.bind)

    def add_student(self, student: StudentCreate) -> StudentRegisterStatus:
        """Добавление студента в бд и создание токена"""
        model_dict = student.model_dump()

        student_id = uuid4()
        student_orm = StudentORM(student_id=student_id, **model_dict)

        self.db.add(student_orm)
        self.db.commit()

        status = StudentRegisterStatus(
            status=True,
            message="ok",
            token=None,
            id=str(student_id)
        )
        return status
    
    def get_student_by_id(self, student_id: UUID) -> Optional[StudentORM]:
        student = (
            self.db.query(StudentORM)
            .filter(StudentORM.student_id == student_id)
            .first()
        )
        return student
    
    def get_student_by_email(self, student_email: str) -> Optional[StudentORM]:
        result = (
            self.db.query(StudentORM)
            .filter(StudentORM.email == student_email)
            .first()
        )
        return result

    
    def patch_student(self, student_id: UUID, student_patch: StudentPatch) -> Optional[StudentORM]:
        changes = student_patch.model_dump(exclude_none=True)
        
        student_orm = self.get_student_by_id(student_id)
        if not student_orm:
            # Обработка случая, когда студент не найден
            return None

        for k, v in changes.items():
            setattr(student_orm, k, v)

        self.db.commit()
        return student_orm
    
    def get_students(self):
        result = (self.db.query(StudentORM).all())
        return result