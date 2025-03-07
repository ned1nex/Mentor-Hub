from pydantic import BaseModel, Field, EmailStr
from pydantic import model_validator
from uuid import UUID
from typing import List, Optional

class MentorRegisterStatus(BaseModel):
    status: bool = Field(..., description="Статус добавления true/false")
    message: str = Field("ok", description="Message добавления")
    token: Optional[str] = Field(None, description="JWT token")
    id: Optional[UUID] = Field(None, description="UUID сущности")

class Password(BaseModel):
    password: str = Field(...)

    @model_validator(mode="after")
    def validate_password(self):
        if len(self.password) < 8:
            raise ValueError("len password should be greater than 8")

        return self

class MentorRegister(Password):
    name: str = Field(..., strict=True, description="Имя ментора")
    email: EmailStr = Field(..., strict=True, description="Email ментора")
    telegram: str = Field(..., strict=True, description="Телеграм ментора")
    expertise: str = Field(..., strict=True, description="Опыт ментора")
    bio: str = Field(..., strict=True, description="О себе")
    score: int = Field(0, strict=True, description="Рейтинг ментора")
    tags: List[str] = Field(..., description="Теги ментора")
    # Ещё пароль


class MentorSignIn(Password):
    email: EmailStr = Field(..., strict=True)
    # Тут ещё пароль


class Mentor(BaseModel):
    mentor_id: str = Field(..., strict=True, description="ID ментора")
    name: str = Field(..., strict=True, description="Имя ментора")
    email: EmailStr = Field(..., strict=True, description="Email ментора")
    telegram: str = Field(..., strict=True, description="Телеграм ментора")
    expertise: str = Field(..., strict=True, description="Опыт ментора")
    bio: str = Field(..., strict=True, description="О себе")
    score: int = Field(0, strict=True, description="Рейтинг ментора")
    tags: List[str] = Field(..., description="Теги ментора")


class MentorSearchResponse(BaseModel):
    mentor: Mentor = Field(...)
    score: float = Field(...)