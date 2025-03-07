from .repository import AdminRepository
from .models import AdminRegisterStatus

from common.dependencies import (
    get_cache_service,
    get_password_token_service
)

class AdminRepositoryService():
    def __init__(self, db, cache):
        self.mentor_repo = AdminRepository(db)
        self.cache_service = get_cache_service(cache)
        self.token_service = get_password_token_service()


    def admin_login(self, mentor_email: str, mentor_password: str) -> AdminRegisterStatus:
        """Проверка ментора на соответствие пароля"""

        admin = self.mentor_repo.get_admin_by_email(mentor_email)
        status = self.token_service.verify_password(mentor_password, admin.password)

        # Если логин пройден - выдаём новый токен (старые удаляются)
        if status:
            token = self.token_service.generate_token(str(admin.admin_id))
            self.cache_service.set_id_with_handler(token=token, id=str(admin.admin_id), handler="admin")

            # Всё ок - возвращаем токен
            return AdminRegisterStatus(
                status=True,
                message="ok",
                token=token,
                id=admin.admin_id
            )
        
        else:
            # Не вошёл в систему
            return AdminRegisterStatus(
                status=False,
                message="not authenticated",
                token=None,
                id=None
            )