from uuid import UUID
from .repository import RequestRepository

from sqlalchemy.orm import Session

class RequestRepositoryService():
    def __init__(self, db: Session) -> None:
        self.repository = RequestRepository(db)

    
    def get_requests_by_mentor_id(self, mentor_id: UUID):
        return self.repository.get_request_by_mentor_id(mentor_id)
    

    def get_requests_by_client_id(self, client_id: UUID):
        return self.repository.get_request_by_client_id(client_id)
    

    def get_all_requests(self):
        return self.repository.get_all_requests()