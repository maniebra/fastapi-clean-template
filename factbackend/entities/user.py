from uuid import UUID
from datetime import date

from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column
from factbackend.generics.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "user_account"

    # Authentication-related user data
    id: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(90))
    email: Mapped[str] = mapped_column(String(90), unique=True)
    phone_number: Mapped[str] = mapped_column(String(14), unique=True)

    # Personal Information
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    # Business Information
    business_name: Mapped[str] = mapped_column(String(50))
    business_location: Mapped[str] = mapped_column(String(50))
    business_type: Mapped[str] = mapped_column(String(50))

    # Auto-generated metadata
    created_at: Mapped[date] = mapped_column(Date)
    updated_at: Mapped[date] = mapped_column(Date)
    last_login: Mapped[date] = mapped_column(Date)
    last_changed_password: Mapped[date] = mapped_column(Date)
