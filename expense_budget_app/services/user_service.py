"""
User service for business logic operations
"""
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from expense_budget_app.models.user import User
from expense_budget_app.schemas.user import UserCreate, UserUpdate
from expense_budget_app.core.security import get_password_hash, verify_password


class UserService:
    """
    Service class for User-related operations
    """

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """
        Get user by ID

        Args:
            db: Database session
            user_id: User ID

        Returns:
            User object or None
        """
        result = await db.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """
        Get user by username

        Args:
            db: Database session
            username: Username

        Returns:
            User object or None
        """
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """
        Get user by email

        Args:
            db: Database session
            email: Email address

        Returns:
            User object or None
        """
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        """
        Create a new user

        Args:
            db: Database session
            user_data: User creation data

        Returns:
            Created User object

        Raises:
            HTTPException: If username or email already exists
        """
        # Check if username already exists
        existing_user = await UserService.get_user_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username '{user_data.username}' already exists"
            )

        # Check if email already exists (if provided)
        if user_data.email:
            existing_email = await UserService.get_user_by_email(db, user_data.email)
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email '{user_data.email}' already exists"
                )

        # Hash password if provided
        hashed_password = None
        if user_data.password:
            hashed_password = get_password_hash(user_data.password)

        # Create user
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            salary=user_data.salary
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return db_user

    @staticmethod
    async def update_user(
        db: AsyncSession,
        user_id: int,
        user_data: UserUpdate
    ) -> User:
        """
        Update user information

        Args:
            db: Database session
            user_id: User ID
            user_data: User update data

        Returns:
            Updated User object

        Raises:
            HTTPException: If user not found or username/email already exists
        """
        # Get existing user
        db_user = await UserService.get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )

        # Check if new username already exists
        if user_data.username and user_data.username != db_user.username:
            existing_user = await UserService.get_user_by_username(db, user_data.username)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Username '{user_data.username}' already exists"
                )

        # Check if new email already exists
        if user_data.email and user_data.email != db_user.email:
            existing_email = await UserService.get_user_by_email(db, user_data.email)
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email '{user_data.email}' already exists"
                )

        # Update fields
        update_data = user_data.model_dump(exclude_unset=True)

        # Hash password if provided
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(db_user, field, value)

        await db.commit()
        await db.refresh(db_user)

        return db_user

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        """
        Delete a user

        Args:
            db: Database session
            user_id: User ID

        Returns:
            True if deleted successfully

        Raises:
            HTTPException: If user not found
        """
        db_user = await UserService.get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )

        await db.delete(db_user)
        await db.commit()

        return True

    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        username: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate user by username and password

        Args:
            db: Database session
            username: Username
            password: Plain password

        Returns:
            User object if authentication successful, None otherwise
        """
        user = await UserService.get_user_by_username(db, username)

        if not user:
            return None

        if not user.hashed_password:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user
