"""
Expense management endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from expense_budget_app.core.security import get_current_user_id
from expense_budget_app.db.session import get_db
from expense_budget_app.schemas.expense import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
    ExpenseFilter
)
from expense_budget_app.schemas.budget import BudgetSummary
from expense_budget_app.services.expense_service import ExpenseService
from expense_budget_app.models.expense import ExpenseCategory
from datetime import date

router = APIRouter()


@router.post(
    "/",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new expense",
    description="Create a new expense entry (requires authentication)"
)
async def create_expense(
    expense_data: ExpenseCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new expense

    Args:
        expense_data: Expense creation data
        current_user_id: Current user ID from JWT token
        db: Database session

    Returns:
        ExpenseResponse: Created expense details

    Raises:
        HTTPException: If user not found, unauthorized, or validation fails
    """
    # Ensure user can only create expenses for themselves
    if expense_data.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create expense for another user"
        )

    expense = await ExpenseService.create_expense(db, expense_data)
    return expense


@router.get(
    "/{user_id}",
    response_model=List[ExpenseResponse],
    summary="Get user's expenses",
    description="Retrieve all expenses for a user with optional filters"
)
async def get_user_expenses(
    user_id: int,
    day: Optional[date] = Query(None, description="Filter by day (YYYY-MM-DD)"),
    week: Optional[int] = Query(None, ge=1, le=53, description="Filter by week number (1-53)"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filter by month (1-12)"),
    year: Optional[int] = Query(None, ge=2000, le=2100, description="Filter by year"),
    category: Optional[ExpenseCategory] = Query(None, description="Filter by category"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all expenses for a user with optional filters

    Args:
        user_id: User ID
        day: Optional filter by specific day
        week: Optional filter by week number (requires year)
        month: Optional filter by month (requires year)
        year: Year for week/month filter
        category: Optional filter by category
        db: Database session

    Returns:
        List[ExpenseResponse]: List of expenses

    Raises:
        HTTPException: If user not found or filter validation fails
    """
    # Create filter object
    filters = ExpenseFilter(
        day=day,
        week=week,
        month=month,
        year=year,
        category=category
    )

    expenses = await ExpenseService.get_user_expenses(db, user_id, filters)
    return expenses


@router.get(
    "/detail/{expense_id}",
    response_model=ExpenseResponse,
    summary="Get expense by ID",
    description="Retrieve expense details by expense ID"
)
async def get_expense(
    expense_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get expense by ID

    Args:
        expense_id: Expense ID
        db: Database session

    Returns:
        ExpenseResponse: Expense details

    Raises:
        HTTPException: If expense not found
    """
    expense = await ExpenseService.get_expense_by_id(db, expense_id)

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with ID {expense_id} not found"
        )

    return expense


@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse,
    summary="Update expense",
    description="Update expense information (requires authentication)"
)
async def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Update expense information

    Args:
        expense_id: Expense ID
        expense_data: Expense update data
        current_user_id: Current user ID from JWT token
        db: Database session

    Returns:
        ExpenseResponse: Updated expense details

    Raises:
        HTTPException: If expense not found or unauthorized
    """
    expense = await ExpenseService.update_expense(
        db,
        expense_id,
        expense_data,
        user_id=current_user_id
    )
    return expense


@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete expense",
    description="Delete an expense (requires authentication)"
)
async def delete_expense(
    expense_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete an expense

    Args:
        expense_id: Expense ID
        current_user_id: Current user ID from JWT token
        db: Database session

    Raises:
        HTTPException: If expense not found or unauthorized
    """
    await ExpenseService.delete_expense(db, expense_id, user_id=current_user_id)


@router.get(
    "/totals/{user_id}",
    response_model=BudgetSummary,
    summary="Get budget summary",
    description="Get budget summary with total expenses, salary, and category breakdown"
)
async def get_budget_summary(
    user_id: int,
    day: Optional[date] = Query(None, description="Filter by day (YYYY-MM-DD)"),
    week: Optional[int] = Query(None, ge=1, le=53, description="Filter by week number (1-53)"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filter by month (1-12)"),
    year: Optional[int] = Query(None, ge=2000, le=2100, description="Filter by year"),
    category: Optional[ExpenseCategory] = Query(None, description="Filter by category"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get budget summary for a user

    Args:
        user_id: User ID
        day: Optional filter by specific day
        week: Optional filter by week number (requires year)
        month: Optional filter by month (requires year)
        year: Year for week/month filter
        category: Optional filter by category
        db: Database session

    Returns:
        BudgetSummary: Budget summary with totals and category breakdown

    Raises:
        HTTPException: If user not found
    """
    # Create filter object
    filters = ExpenseFilter(
        day=day,
        week=week,
        month=month,
        year=year,
        category=category
    )

    summary = await ExpenseService.get_budget_summary(db, user_id, filters)
    return summary
