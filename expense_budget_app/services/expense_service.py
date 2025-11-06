"""
Expense service for business logic operations
"""
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from expense_budget_app.models.expense import Expense, ExpenseCategory
from expense_budget_app.models.user import User
from expense_budget_app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseFilter
from expense_budget_app.schemas.budget import BudgetSummary, CategoryBreakdown


class ExpenseService:
    """
    Service class for Expense-related operations
    """

    @staticmethod
    async def verify_user_exists(db: AsyncSession, user_id: int) -> User:
        """
        Verify if user exists

        Args:
            db: Database session
            user_id: User ID

        Returns:
            User object

        Raises:
            HTTPException: If user not found
        """
        result = await db.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )

        return user

    @staticmethod
    async def create_expense(
        db: AsyncSession,
        expense_data: ExpenseCreate
    ) -> Expense:
        """
        Create a new expense

        Args:
            db: Database session
            expense_data: Expense creation data

        Returns:
            Created Expense object

        Raises:
            HTTPException: If user not found or validation fails
        """
        # Verify user exists
        await ExpenseService.verify_user_exists(db, expense_data.user_id)

        # Create expense
        db_expense = Expense(
            user_id=expense_data.user_id,
            name=expense_data.name,
            amount=expense_data.amount,
            category=expense_data.category
        )

        db.add(db_expense)
        await db.commit()
        await db.refresh(db_expense)

        return db_expense

    @staticmethod
    async def get_expense_by_id(
        db: AsyncSession,
        expense_id: int
    ) -> Optional[Expense]:
        """
        Get expense by ID

        Args:
            db: Database session
            expense_id: Expense ID

        Returns:
            Expense object or None
        """
        result = await db.execute(
            select(Expense).where(Expense.expense_id == expense_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_expenses(
        db: AsyncSession,
        user_id: int,
        filters: Optional[ExpenseFilter] = None
    ) -> List[Expense]:
        """
        Get all expenses for a user with optional filters

        Args:
            db: Database session
            user_id: User ID
            filters: Optional filter parameters

        Returns:
            List of Expense objects

        Raises:
            HTTPException: If user not found
        """
        # Verify user exists
        await ExpenseService.verify_user_exists(db, user_id)

        # Build query
        query = select(Expense).where(Expense.user_id == user_id)

        # Apply filters
        if filters:
            conditions = []

            # Filter by day
            if filters.day:
                start_of_day = datetime.combine(filters.day, datetime.min.time())
                end_of_day = datetime.combine(filters.day, datetime.max.time())
                conditions.append(
                    and_(
                        Expense.created_at >= start_of_day,
                        Expense.created_at <= end_of_day
                    )
                )

            # Filter by week
            elif filters.week and filters.year:
                # Calculate start and end of week
                jan_1 = datetime(filters.year, 1, 1)
                week_start = jan_1 + timedelta(weeks=filters.week - 1)
                week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)

                conditions.append(
                    and_(
                        Expense.created_at >= week_start,
                        Expense.created_at <= week_end
                    )
                )

            # Filter by month
            elif filters.month and filters.year:
                # Calculate start and end of month
                month_start = datetime(filters.year, filters.month, 1)

                if filters.month == 12:
                    month_end = datetime(filters.year + 1, 1, 1) - timedelta(seconds=1)
                else:
                    month_end = datetime(filters.year, filters.month + 1, 1) - timedelta(seconds=1)

                conditions.append(
                    and_(
                        Expense.created_at >= month_start,
                        Expense.created_at <= month_end
                    )
                )

            # Filter by category
            if filters.category:
                conditions.append(Expense.category == filters.category)

            if conditions:
                query = query.where(and_(*conditions))

        # Order by created_at descending
        query = query.order_by(Expense.created_at.desc())

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def update_expense(
        db: AsyncSession,
        expense_id: int,
        expense_data: ExpenseUpdate,
        user_id: Optional[int] = None
    ) -> Expense:
        """
        Update an expense

        Args:
            db: Database session
            expense_id: Expense ID
            expense_data: Expense update data
            user_id: Optional user ID for authorization check

        Returns:
            Updated Expense object

        Raises:
            HTTPException: If expense not found or unauthorized
        """
        db_expense = await ExpenseService.get_expense_by_id(db, expense_id)

        if not db_expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Expense with ID {expense_id} not found"
            )

        # Check authorization if user_id provided
        if user_id and db_expense.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this expense"
            )

        # Update fields
        update_data = expense_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_expense, field, value)

        await db.commit()
        await db.refresh(db_expense)

        return db_expense

    @staticmethod
    async def delete_expense(
        db: AsyncSession,
        expense_id: int,
        user_id: Optional[int] = None
    ) -> bool:
        """
        Delete an expense

        Args:
            db: Database session
            expense_id: Expense ID
            user_id: Optional user ID for authorization check

        Returns:
            True if deleted successfully

        Raises:
            HTTPException: If expense not found or unauthorized
        """
        db_expense = await ExpenseService.get_expense_by_id(db, expense_id)

        if not db_expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Expense with ID {expense_id} not found"
            )

        # Check authorization if user_id provided
        if user_id and db_expense.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this expense"
            )

        await db.delete(db_expense)
        await db.commit()

        return True

    @staticmethod
    async def get_budget_summary(
        db: AsyncSession,
        user_id: int,
        filters: Optional[ExpenseFilter] = None
    ) -> BudgetSummary:
        """
        Get budget summary for a user

        Args:
            db: Database session
            user_id: User ID
            filters: Optional filter parameters

        Returns:
            BudgetSummary object with totals and category breakdown

        Raises:
            HTTPException: If user not found
        """
        # Verify user exists and get salary
        user = await ExpenseService.verify_user_exists(db, user_id)

        # Get expenses with filters
        expenses = await ExpenseService.get_user_expenses(db, user_id, filters)

        # Calculate total expense
        total_expense = sum(expense.amount for expense in expenses)

        # Calculate remaining amount
        remaining_amount = user.salary - total_expense

        # Calculate category breakdown
        category_totals: Dict[str, float] = {
            ExpenseCategory.FOOD.value: 0.0,
            ExpenseCategory.TRANSPORT.value: 0.0,
            ExpenseCategory.ENTERTAINMENT.value: 0.0,
            ExpenseCategory.UTILITIES.value: 0.0,
            ExpenseCategory.OTHER.value: 0.0,
        }

        for expense in expenses:
            category_totals[expense.category.value] += expense.amount

        category_breakdown = CategoryBreakdown(**category_totals)

        return BudgetSummary(
            user_id=user_id,
            total_salary=user.salary,
            total_expense=round(total_expense, 2),
            remaining_amount=round(remaining_amount, 2),
            category_breakdown=category_breakdown
        )
