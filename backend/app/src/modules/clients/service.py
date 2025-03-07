# Бизнес логика
from .models import StudentRegisterStatus
from .repository import StudentRepository

from common.dependencies import (
    get_cache_service,
    get_password_token_service
)

from sqlalchemy.orm import Session
from redis import Redis

class StudentRepositoryService():
    def __init__(self, db: Session, cache: Redis):
        self.student_repo = StudentRepository(db, cache)
        self.token_service = get_password_token_service()
        self.cache_service = get_cache_service(cache)

    def student_login(self, student_email: str, student_password: str) -> StudentRegisterStatus:
        """Проверка пароля студента"""
        try:
            student = self.student_repo.get_student_by_email(student_email)
            if not student:
                print(f"[ERROR] Student with email {student_email} not found.")
                return StudentRegisterStatus(
                    status=False, message="student not found", token=None, id=None
                )

            if not student.password:
                print(f"[ERROR] Student {student_email} has no password stored.")
                return StudentRegisterStatus(
                    status=False, message="password is missing", token=None,
                    id=str(student.student_id) if student.student_id else None  # 🔥 UUID -> str
                )

            # Проверяем пароль
            status = self.token_service.verify_password(student_password, student.password)
            if not status:
                print(f"[ERROR] Password verification failed for {student_email}.")
                return StudentRegisterStatus(
                    status=False, message="not authenticated", token=None,
                    id=str(student.student_id) if student.student_id else None  # 🔥 UUID -> str
                )

            # Генерируем новый токен
            if not student.student_id:
                print(f"[CRITICAL ERROR] Student ID is missing for {student_email}.")
                return StudentRegisterStatus(
                    status=False, message="internal error: missing student ID", token=None, id=None
                )

            token = self.token_service.generate_token(str(student.student_id))  # 🔥 UUID -> str
            self.cache_service.set_id_with_handler(token=token, id=str(student.student_id), handler="student")  # 🔥 UUID -> str

            print(f"[INFO] Student {student_email} logged in successfully.")

            return StudentRegisterStatus(
                status=True, message="ok", token=token, id=str(student.student_id)  # 🔥 UUID -> str
            )

        except Exception as e:
            print(f"[CRITICAL ERROR] Unexpected error in student_login(): {e}")
            return StudentRegisterStatus(
                status=False, message=f"internal server error: {str(e)}", token=None, id=None
            )
