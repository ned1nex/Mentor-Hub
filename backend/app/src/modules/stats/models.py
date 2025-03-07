from typing import Optional
from pydantic import BaseModel, Field, model_validator

from enum import Enum

class Status(Enum):
    ACCEPTED = "ACCEPTED"
    REFUSED = "REFUSED"
    PENDING = "PENDING"


class MentorStats(BaseModel):
    accepted: int = Field(..., description="Сколько заявок было принято")
    refused: int = Field(..., description="Сколько заявок было отклнонено")
    pending: int = Field(..., description="Сколько заявок ожидает")
    total: Optional[int] = Field(0, description="Сколько всего заявок")

    @model_validator(mode="after")
    def fill_total(self):
        self.total = (
            self.accepted + self.refused + self.pending
        )
        return self
    

class AdminStats(BaseModel):
    total_students: int = Field(..., description="Полное количество студентов")
    total_mentors: int = Field(..., description="Полное количество менторов")
    accepted: int = Field(..., description="Полное количество одобренных заявок")
    refused: int = Field(..., description="Полное количество отклоненных заявок")
    pending: int = Field(..., description="Количество ожидающих заявок")