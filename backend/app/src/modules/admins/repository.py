from uuid import uuid4
from .schemas import Base, AdminORM
from .models import Admin, AdminCreate, AdminRegisterStatus

from sqlalchemy.orm import Session


class AdminRepository():
    def __init__(self, db: Session) -> None:
        self.db = db
        Base.metadata.create_all(db.bind)


    def add_admin(self, admin: AdminCreate):
        model_dict = admin.model_dump()

        admin_id = str(uuid4())
        admin_orm = AdminORM(admin_id=admin_id, **model_dict)

        self.db.add(admin_orm)
        self.db.commit

        return AdminRegisterStatus(
            status=True,
            message="ok",
            token=None,
            id=admin_id
        )
    
    def get_admin_by_email(self, email: str):
        result = (self.db.query(AdminORM).filter(AdminORM.email == email).first())
        return result