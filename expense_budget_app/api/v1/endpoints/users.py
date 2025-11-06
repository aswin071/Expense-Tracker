"""
User management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from expense_budget_app.core.security import get_current_user_id
from expense_budget_app.db.session import get_db
from expense_budget_app.schemas.user import UserCreate, UserUpdate, UserResponse
from expense_budget_app.services.user_service import UserService

router = APIRouter()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with username and optional salary"
)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new user

    Args:
        user_data: User creation data (username, optional email, password, salary)
        db: Database session

    Returns:
        UserResponse: Created user details

    Raises:
        HTTPException: If username or email already exists
    """
    user = await UserService.create_user(db, user_data)
    return user


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve user details by user ID"
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user by ID

    Args:
        user_id: User ID
        db: Database session

    Returns:
        UserResponse: User details

    Raises:
        HTTPException: If user not found
    """
    user = await UserService.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    return user


@router.get(
    "/me/profile",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Get the profile of the currently authenticated user"
)
async def get_current_user_profile(
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current authenticated user's profile

    Args:
        current_user_id: Current user ID from JWT token
        db: Database session

    Returns:
        UserResponse: Current user details

    Raises:
        HTTPException: If user not found
    """
    user = await UserService.get_user_by_id(db, current_user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description="Update user information (requires authentication)"
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Update user information

    Args:
        user_id: User ID to update
        user_data: User update data
        current_user_id: Current user ID from JWT token
        db: Database session

    Returns:
        UserResponse: Updated user details

    Raises:
        HTTPException: If user not found, unauthorized, or validation fails
    """
    # Check authorization - users can only update their own profile
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )

    user = await UserService.update_user(db, user_id, user_data)
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete user account (requires authentication)"
)
async def delete_user(
    user_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete user account

    Args:
        user_id: User ID to delete
        current_user_id: Current user ID from JWT token
        db: Database session

    Raises:
        HTTPException: If user not found or unauthorized
    """
    # Check authorization - users can only delete their own account
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )

    await UserService.delete_user(db, user_id)
