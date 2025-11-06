"""
Expense Pydantic schemas for request/response validation
"""
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from expense_budget_app.models.expense import ExpenseCategory


class ExpenseBase(BaseModel):
    """
    Base Expense schema with common attributes
    """
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Expense name/description"
    )
    amount: float = Field(
        ...,
        gt=0,
        description="Expense amount (must be > 0)"
    )
    category: ExpenseCategory = Field(
        ...,
        description="Expense category"
    )


class ExpenseCreate(ExpenseBase):
    """
    Schema for creating a new expense
    """
    user_id: int = Field(..., gt=0, description="User ID")

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return round(v, 2)

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "name": "Grocery shopping",
                "amount": 150.50,
                "category": "Food"
            }
        }
    }


class ExpenseUpdate(BaseModel):
    """
    Schema for updating an expense
    """
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200
    )
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[ExpenseCategory] = None

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Amount must be greater than 0")
        return round(v, 2) if v is not None else v


class ExpenseResponse(ExpenseBase):
    """
    Schema for expense response
    """
    expense_id: int
    user_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "expense_id": 1,
                "user_id": 1,
                "name": "Grocery shopping",
                "amount": 150.50,
                "category": "Food",
                "created_at": "2025-01-01T10:00:00"
            }
        }
    }


class ExpenseFilter(BaseModel):
    """
    Schema for filtering expenses
    """
    day: Optional[date] = Field(
        None,
        description="Filter by specific day (YYYY-MM-DD)"
    )
    week: Optional[int] = Field(
        None,
        ge=1,
        le=53,
        description="Filter by week number (1-53)"
    )
    month: Optional[int] = Field(
        None,
        ge=1,
        le=12,
        description="Filter by month (1-12)"
    )
    year: Optional[int] = Field(
        None,
        ge=2000,
        le=2100,
        description="Filter by year"
    )
    category: Optional[ExpenseCategory] = Field(
        None,
        description="Filter by category"
    )

    @field_validator('week')
    @classmethod
    def validate_week_requires_year(cls, v, info):
        if v is not None and info.data.get('year') is None:
            raise ValueError("Year is required when filtering by week")
        return v

    @field_validator('month')
    @classmethod
    def validate_month_requires_year(cls, v, info):
        if v is not None and info.data.get('year') is None:
            raise ValueError("Year is required when filtering by month")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "day": "2025-01-15",
                "category": "Food"
            }
        }
    }
