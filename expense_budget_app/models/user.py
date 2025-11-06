"""
User model
"""
from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Float, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from expense_budget_app.db.base import Base

if TYPE_CHECKING:
    from expense_budget_app.models.expense import Expense


class User(Base):
    """
    User model for storing user information and salary

    Attributes:
        user_id: Primary key, auto-incremented
        username: Unique username for the user
        email: Optional email address
        hashed_password: Hashed password for authentication
        salary: User's monthly/annual salary (default: 0.0)
        is_active: Whether the user account is active
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment="Primary key"
    )
    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
        comment="Unique username"
    )
    email: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        index=True,
        comment="User email address"
    )
    hashed_password: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Hashed password"
    )
    salary: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
        comment="User's salary"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Account active status"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Creation timestamp"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="Last update timestamp"
    )

    # Relationship with expenses
    expenses: Mapped[List["Expense"]] = relationship(
        "Expense",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<User(user_id={self.user_id}, username='{self.username}', salary={self.salary})>"
