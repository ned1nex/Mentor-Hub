#pydentic models 
from pydantic import BaseModel, EmailStr, Field
from pydantic import model_validator, field_serializer, field_validator
from uuid import UUID

from typing import Optional

class StudentRegisterStatus(BaseModel):
    status: bool = Field(..., description="Статус добавления true/false")
    message: str = Field("ok", description="Сообщение")
    token: Optional[str] = Field(None, description="JWT token")
    id: Optional[str] = Field(None, description="UUID в строковом формате")  # Делаем id строкой

    # Автоматически преобразуем UUID в строку
    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        if isinstance(data.get("id"), UUID):
            data["id"] = str(data["id"])  # Преобразуем UUID в строку
        return data


class Password(BaseModel):
    password: str = Field(...)

    @model_validator(mode="after")
    def validate_password(self):
        if len(self.password) < 8:
            raise ValueError("len password should be greater than 8")

        return self

class StudentCreate(Password):
    email: EmailStr = Field(..., strict=True)
    name: str = Field(..., strict=True)
    password: str = Field(..., strict=True)
    telegram: str = Field(..., strict=True)

    age: Optional[int] = Field(None, strict=True, ge=0, le=100)
    bio: Optional[str] = Field(None, strict=True)


class Student(StudentCreate):
    """Моделька для студента"""
    email: EmailStr = Field(..., strict=True)
    name: str = Field(..., strict=True)
    password: str = Field(..., strict=True)
    telegram: str = Field(..., strict=True)



class StudentPatch(BaseModel):
    """Модель для изменения параметров студента"""
    name: Optional[str] = Field(None, strict=True, description="Имя студента")
    password: Optional[str] = Field(None, strict=True, description="Пароль с аккаунту студента")
    telegram: Optional[str] = Field(None, strict=True, description="Телеграм студента")
    age: Optional[int] = Field(None, strict=True, description="Возраст")
    bio: Optional[str] = Field(None, strict=True, description="Био студента")


    @model_validator(mode="after")
    def validate_password(self):
        if self.password:
            # Проверка пароля
            if len(self.password) < 8:
                raise ValueError("len password should be greater than 8")

        return self


class StudentSignIn(Password):
    email: EmailStr = Field(..., strict=True)


class StudentOut(BaseModel):
    student_id: str
    email: str
    name: str
    telegram: str
    age: Optional[int]
    bio: Optional[str]

    class Config:
        from_attributes = True

    @field_validator("student_id", mode="before")
    def convert_student_id(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v

    @field_serializer("student_id", mode="plain")
    def serialize_student_id(self, value: str) -> str:
        return value