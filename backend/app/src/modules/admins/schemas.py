from sqlalchemy import UUID, Column, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


class AdminORM(Base):
    __tablename__ = "admins"

    admin_id = Column("admin_id", UUID, primary_key=True)
    email = Column("email", String)
    password = Column("password", String)