# Работа с репозиторием (бд)

from uuid import UUID
from sqlalchemy.orm import Session
from redis import Redis

import random

from uuid import uuid4
from typing import List, Optional, Any

from .models import MentorRegister, MentorRegisterStatus
from .schemas import MentorORM, Base


class MentorRepository():
    def __init__(self, db: Session, cache: Redis):
        self.db = db
        Base.metadata.create_all(db.bind)

    def get_mentor_by_id(self, mentor_id: UUID) -> Optional[MentorORM]:
        """Получение ментора по его ID"""
        result = (
            self.db.query(MentorORM)
            .filter(MentorORM.mentor_id == mentor_id)
            .first()
        )
        return result
    
    def get_mentor_by_email(self, mentor_email: str) -> Optional[MentorORM]:
        """Получение ментора по его емейлу"""
        result = (
            self.db.query(MentorORM)
            .filter(MentorORM.email == mentor_email)
            .first()
        )
        
        return result

    
    def add_mentor(self, mentor: MentorRegister) -> MentorRegisterStatus:
        """Добавляет ментора в бд и кеш -> JWT Token"""
        model_dict = mentor.model_dump()

        mentor_id = uuid4()
        model_orm = MentorORM(
            mentor_id=mentor_id,  
            **model_dict
        )

        self.db.add(model_orm)
        self.db.commit()

        return MentorRegisterStatus(
            status=True,
            message="ok",
            token=None,
            id=mentor_id
        )
    

    def get_mentors(self) -> List[MentorORM]:
        """Получение всех менторов впринципе"""
        result = self.db.query(MentorORM).all()
        return result
    

    def add_score(self, mentor_id: str, score: int) -> Optional[MentorORM]:
        mentor = (
            self.db.query(MentorORM)
            .filter(MentorORM.mentor_id == mentor_id)
            .first()
        )
        if not mentor:
            return None

        updated_score = mentor.score + score
        setattr(mentor, "score", updated_score)
        self.db.commit()

        return mentor