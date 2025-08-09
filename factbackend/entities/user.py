import datetime
from typing import final
from uuid import UUID
from datetime import date
import uuid

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from factbackend.generics.base_model import BaseModel


@final
class User(BaseModel):
    __tablename__ = "user_account"

    # Authentication-related user data
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(90))
    email: Mapped[str] = mapped_column(String(90), unique=True)
    phone_number: Mapped[str] = mapped_column(String(14), unique=True)

    # Personal Information
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    # Auto-generated metadata
    created_at: Mapped[date] = mapped_column(DateTime, default=datetime.datetime.now())
    updated_at: Mapped[date] = mapped_column(DateTime, nullable=True, default=None)
    last_login: Mapped[date] = mapped_column(DateTime, nullable=True, default=None)
    last_changed_password: Mapped[date] = mapped_column(
        DateTime, nullable=True, default=None
    )
