import datetime
from typing import final
from uuid import UUID
from datetime import date
import uuid

from sqlalchemy import (
    Constraint,
    DateTime,
    ForeignKey,
    String,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from src.commons.generics.base_entity import BaseEntity


@final
class UserRole(BaseEntity):
    __tablename__: str = "user_roles"
    __table_args__: tuple[Constraint] = (UniqueConstraint("user_id", "role_id"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE"), primary_key=True
    )
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    )

    assigned_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now()
    )

    user: Mapped["User"] = relationship(back_populates="user_roles")
    role: Mapped["Role"] = relationship(back_populates="role_users", lazy="joined")


@final
class User(BaseEntity):
    __tablename__: str = "user_account"

    # Authentication-related user data
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(90))
    email: Mapped[str] = mapped_column(String(90), unique=True)
    phone_number: Mapped[str] = mapped_column(String(14), unique=True)
    user_roles: Mapped[list["UserRole"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )

    roles: AssociationProxy[list["Role"]] = association_proxy("user_roles", "role")

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


@final
class Role(BaseEntity):
    __tablename__: str = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    role_users: Mapped[list["UserRole"]] = relationship(
        back_populates="role", cascade="all, delete-orphan"
    )

    users: Mapped[list["User"]] = relationship(secondary="user_roles", viewonly=True)
