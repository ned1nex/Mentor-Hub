from pydantic import BaseModel, Field, model_validator
from uuid import UUID


class RoleResponse(BaseModel):
    role: str = Field(..., strict=True, description="Роль объекта в системе")
    id: str = Field(..., strict=True, description="UUID объекта в системе")


class CalendarModel(BaseModel):
    date: str = Field(..., strict=True, description="Дата в формате YYYY-MM-DD")


class CalendarResponse(BaseModel):
    file: str