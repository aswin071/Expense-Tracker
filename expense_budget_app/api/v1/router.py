"""
Main API router that aggregates all endpoint routers
"""
from fastapi import APIRouter

from expense_budget_app.api.v1.endpoints import auth, users, expenses

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

api_router.include_router(
    expenses.router,
    prefix="/expenses",
    tags=["Expenses"]
)
