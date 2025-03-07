from redis import Redis
from sqlalchemy.orm import Session

from ..repository import StudentRepository


class StudentRepositoryService():
    def __init__(self, db: Session, cache: Redis) -> None:
        self.repository = StudentRepository(db, cache)

    def get_student_by_id(self, student_id):
        return self.repository.get_student_by_id(student_id)
    
    def get_students(self):
        return self.repository.get_students()