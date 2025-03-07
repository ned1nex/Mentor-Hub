from re import S
from uuid import UUID

from redis import Redis

from common.dependencies import (
    get_request_service,
    get_mentor_service,
    get_student_service
)

from .models import Status, MentorStats, AdminStats
from sqlalchemy.orm import Session


"""
Статистики:
у ментора:
- total users
- accepted
- refused
- rating

"""


class StatisticsService():
    def __init__(self, db: Session, cache: Redis) -> None:
        self.request_repository = get_request_service(db)
        self.mentor_service = get_mentor_service(db, cache)
        self.student_service = get_student_service(db, cache)


    def get_mentor_statistics(self, mentor_id: UUID):
        requests = self.request_repository.get_requests_by_mentor_id(mentor_id)

        accepted = len([r for r in requests if r.status == Status.ACCEPTED.value])
        refused = len([r for r in requests if r.status == Status.REFUSED.value])
        pending = len([r for r in requests if r.status == Status.PENDING.value])

        stats = MentorStats(
            accepted=accepted,
            refused=refused,
            pending=pending,
            total=0
        )
        return stats
    

    def get_administrator_stats(self):
        requests = self.request_repository.get_all_requests()

        accepted = len([r for r in requests if r.status == Status.ACCEPTED.value])
        refused = len([r for r in requests if r.status == Status.REFUSED.value])
        pending = len([r for r in requests if r.status == Status.PENDING.value])

        stats = AdminStats(
            total_students=len(self.student_service.get_students()),
            total_mentors=len(self.mentor_service.get_mentors()),
            accepted=accepted,
            refused=refused,
            pending=pending
        )
        return stats