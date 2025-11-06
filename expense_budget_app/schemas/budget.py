"""
Budget summary Pydantic schemas
"""
from typing import Dict
from pydantic import BaseModel, Field


class CategoryBreakdown(BaseModel):
    """
    Schema for category-wise expense breakdown
    """
    Food: float = Field(default=0.0, ge=0)
    Transport: float = Field(default=0.0, ge=0)
    Entertainment: float = Field(default=0.0, ge=0)
    Utilities: float = Field(default=0.0, ge=0)
    Other: float = Field(default=0.0, ge=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "Food": 1500.50,
                "Transport": 500.00,
                "Entertainment": 300.00,
                "Utilities": 800.00,
                "Other": 200.00
            }
        }
    }


class BudgetSummary(BaseModel):
    """
    Schema for budget summary response
    """
    user_id: int = Field(..., description="User ID")
    total_salary: float = Field(..., ge=0, description="Total salary")
    total_expense: float = Field(..., ge=0, description="Total expenses")
    remaining_amount: float = Field(..., description="Remaining amount (salary - expenses)")
    category_breakdown: CategoryBreakdown = Field(..., description="Expenses by category")

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "total_salary": 50000.00,
                "total_expense": 3300.50,
                "remaining_amount": 46699.50,
                "category_breakdown": {
                    "Food": 1500.50,
                    "Transport": 500.00,
                    "Entertainment": 300.00,
                    "Utilities": 800.00,
                    "Other": 200.00
                }
            }
        }
    }
