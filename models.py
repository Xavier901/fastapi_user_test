from sqlalchemy import Column, Integer, String
# from database import  Base
from base import Base


class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from typing import cast
from sqlalchemy import Column
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import Boolean


# class UserTable(AsyncAttrs, SQLAlchemyBaseUserTableUUID, Base):
#     is_superuser: bool = cast(bool, mapped_column(Boolean, default=False, nullable=False))

class UserTable(SQLAlchemyBaseUserTableUUID, Base):
    pass
#    # __tablename__ = "users"


