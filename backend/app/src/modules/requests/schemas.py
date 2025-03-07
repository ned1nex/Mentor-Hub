from sqlalchemy import Boolean, Column, String, UUID, DateTime, func
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


class RequestORM(Base):
    __tablename__ = "request_table"

    request_id = Column("request_id", UUID, primary_key=True)
    student_id = Column("client_id", UUID, primary_key=True)
    mentor_id = Column("mentor_id", UUID, primary_key=True)

    query = Column("query", String)
    status = Column("status", String) # accepted / refused / pending
    date = Column("date", DateTime)


    def to_dict(self):
        model_dict = {
            "request_id": str(self.request_id),
            "student_id": str(self.student_id),
            "mentor_id": str(self.mentor_id),

            "query": self.query,
            "status": self.status,
            "date": self.date
        }
        return model_dict