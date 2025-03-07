from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

from enum import Enum

class Status(Enum):
    ACCEPTED = "ACCEPTED"
    REFUSED = "REFUSED"
    PENDING = "PENDING"


class RequestCreateResponse(BaseModel):
    request_id: UUID = Field(..., description="ID заявки")


class RequestCreate(BaseModel):
    mentor_id: UUID = Field(..., description="ID ментора")
    student_id: UUID = Field(..., description="ID клиента")

    query: str = Field(..., description="Вопрос пользователя")
    status: Status = Field(Status.PENDING, description="Статус заявки pending / accepted / refused")
    date: datetime = Field(
        ...,
        description="Дата в формате YY-MM-DD",
        json_schema_extra={"format": "yy-mm-dd"}
    )


class RequestPatch(BaseModel):
    query: Optional[str] = Field(None, description="Запрос юзера")
    status: Optional[str] = Field(None, description="Статус заявки")
    date: Optional[datetime] = Field(
        None,
        description="Дата в формате YY-MM-DD",
        json_schema_extra={"format": "yy-mm-dd"}
    )


class Request(BaseModel):
    request_id: UUID = Field(..., description="ID заявки")
    mentor_id: UUID = Field(..., description="ID ментора")
    student_id: UUID = Field(..., description="ID клиента")

    query: str = Field(..., description="Вопрос пользователя")
    status: Status = Field(Status.PENDING, description="Статус заявки pending / accepted / refused")
    date: datetime = Field(
        ...,
        description="Дата в формате YY-MM-DD",
        json_schema_extra={"format": "yy-mm-dd"}
    )
