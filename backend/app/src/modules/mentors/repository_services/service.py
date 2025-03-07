from uuid import UUID
from redis import Redis
from ..repository import MentorRepository

from sqlalchemy.orm import Session

class MentorRepositoryService:
    def __init__(self, db: Session, cache: Redis) -> None:
        self.repository = MentorRepository(db, cache)

    def get_mentor_by_id(self, mentor_id: UUID):
        return self.repository.get_mentor_by_id(mentor_id)
    
    def get_mentors(self):
        return self.repository.get_mentors()