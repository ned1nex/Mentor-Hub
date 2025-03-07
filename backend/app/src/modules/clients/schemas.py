from typing import Dict

from sqlalchemy import Column, Integer, String, Text, UUID, null
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


class StudentORM(Base):
    __tablename__ = 'students'
    
    student_id = Column("student_id", UUID, primary_key=True)
    email = Column("email", String, nullable=False)
    name = Column("name", String, nullable=False)
    password = Column("password", String, nullable=False)
    telegram = Column("telegram", String, nullable=False)
                      
    age = Column("age", Integer, nullable=True)
    bio = Column("bio", Text, nullable=True)

    def to_dict(self) -> Dict:
        model_dict = {
            "student_id": str(self.student_id),
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "age": self.age,
            "bio": self.bio,
            "telegram": self.telegram
        }
        return model_dict
    
