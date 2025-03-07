from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID

class AdminRegisterStatus(BaseModel):
    status: bool = Field(..., examples=[True, False], description="Статус добавления true/false")
    message: str = Field("ok", description="Message добавления")
    token: Optional[str] = Field(None, description="JWT token")
    id: Optional[UUID] = Field(None, description="UUID сущности")


class AdminCreate(BaseModel):
    email: EmailStr = Field(..., description="Емейл админа")
    password: str = Field(..., description="Пароль админа")


class Admin(BaseModel):
    admin_id: UUID = Field(..., description="ID админа")
    email: EmailStr = Field(..., description="Емейл админа")
    password: str = Field(..., description="Пароль админа")