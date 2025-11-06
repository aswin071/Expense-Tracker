"""
User Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator


class UserBase(BaseModel):
    """
    Base User schema with common attributes
    """
    username: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Username (3-100 characters)"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="User email address"
    )


class UserCreate(UserBase):
    """
    Schema for creating a new user
    """
    password: Optional[str] = Field(
        None,
        min_length=8,
        max_length=100,
        description="Password (min 8 characters)"
    )
    salary: float = Field(
        default=0.0,
        ge=0,
        description="User's salary (must be >= 0)"
    )

    @field_validator('salary')
    @classmethod
    def validate_salary(cls, v):
        if v < 0:
            raise ValueError("Salary must be non-negative")
        return v


class UserUpdate(BaseModel):
    """
    Schema for updating user information
    """
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100
    )
    email: Optional[EmailStr] = None
    salary: Optional[float] = Field(None, ge=0)
    password: Optional[str] = Field(
        None,
        min_length=8,
        max_length=100
    )

    @field_validator('salary')
    @classmethod
    def validate_salary(cls, v):
        if v is not None and v < 0:
            raise ValueError("Salary must be non-negative")
        return v


class UserResponse(UserBase):
    """
    Schema for user response
    """
    user_id: int
    salary: float
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "salary": 50000.0,
                "is_active": True,
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00"
            }
        }
    }


class UserLogin(BaseModel):
    """
    Schema for user login
    """
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "john_doe",
                "password": "secretpassword"
            }
        }
    }
