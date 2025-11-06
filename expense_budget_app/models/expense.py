"""
Expense model and category enum
"""
import enum
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import (
    String,
    Float,
    DateTime,
    ForeignKey,
    Enum as SQLEnum,
    Index
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from expense_budget_app.db.base import Base

if TYPE_CHECKING:
    from expense_budget_app.models.user import User


class ExpenseCategory(str, enum.Enum):
    """
    Enum for expense categories
    """
    FOOD = "Food"
    TRANSPORT = "Transport"
    ENTERTAINMENT = "Entertainment"
    UTILITIES = "Utilities"
    OTHER = "Other"


class Expense(Base):
    """
    Expense model for tracking user expenses

    Attributes:
        expense_id: Primary key, auto-incremented
        user_id: Foreign key to User table
        name: Name/description of the expense
        amount: Expense amount (must be > 0)
        category: Category of expense (Food/Transport/Entertainment/Utilities/Other)
        created_at: Timestamp when expense was created
    """
    __tablename__ = "expenses"

    expense_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment="Primary key"
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Foreign key to users table"
    )
    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="Expense name/description"
    )
    amount: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Expense amount"
    )
    category: Mapped[ExpenseCategory] = mapped_column(
        SQLEnum(ExpenseCategory),
        nullable=False,
        index=True,
        comment="Expense category"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
        comment="Creation timestamp"
    )

    # Relationship with user
    user: Mapped["User"] = relationship("User", back_populates="expenses")

    # Composite indexes for efficient querying
    __table_args__ = (
        Index('idx_user_created', 'user_id', 'created_at'),
        Index('idx_user_category', 'user_id', 'category'),
        Index('idx_user_created_category', 'user_id', 'created_at', 'category'),
    )

    def __repr__(self) -> str:
        return (
            f"<Expense(expense_id={self.expense_id}, "
            f"user_id={self.user_id}, "
            f"name='{self.name}', "
            f"amount={self.amount}, "
            f"category='{self.category.value}')>"
        )
