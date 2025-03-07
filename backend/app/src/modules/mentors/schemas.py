# Схемы ORM

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, UUID, Integer, String, Float, ARRAY

class Base(DeclarativeBase):
    pass


class MentorORM(Base):
    __tablename__ = "campaigns"

    mentor_id = Column("mentor_id", UUID, primary_key=True)
    name = Column("name", String)
    email = Column("email", String)
    telegram = Column("telegram", String)
    password = Column("password", String)
    expertise = Column("expertise", String)
    bio = Column("bio", String)
    score = Column("score", Integer)
    tags = Column("tags", ARRAY(String))

    def to_dict(self):
        model_dict = {
            "mentor_id": str(self.mentor_id),
            "name": self.name,
            "telegram": self.telegram,
            "email": self.email,
            "expertise": self.expertise,
            "bio": self.bio,
            "score": self.score,
            "tags": self.tags
        }
        return model_dict
