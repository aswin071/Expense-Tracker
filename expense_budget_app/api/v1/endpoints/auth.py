"""
Authentication endpoints
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from expense_budget_app.core.config import settings
from expense_budget_app.core.security import create_access_token, create_refresh_token
from expense_budget_app.db.session import get_db
from expense_budget_app.schemas.token import Token
from expense_budget_app.schemas.user import UserLogin
from expense_budget_app.services.user_service import UserService

router = APIRouter()


@router.post(
    "/login",
    response_model=Token,
    summary="User login",
    description="Authenticate user and return JWT tokens"
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    User login endpoint using OAuth2 password flow

    Args:
        form_data: OAuth2 form with username and password
        db: Database session

    Returns:
        Token: Access and refresh tokens

    Raises:
        HTTPException: If credentials are invalid
    """
    # Authenticate user
    user = await UserService.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Create tokens
    access_token = create_access_token(
        data={"sub": str(user.user_id), "username": user.username}
    )

    refresh_token = create_refresh_token(
        data={"sub": str(user.user_id), "username": user.username}
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post(
    "/login-json",
    response_model=Token,
    summary="User login (JSON)",
    description="Authenticate user with JSON body and return JWT tokens"
)
async def login_json(
    user_login: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    User login endpoint using JSON body

    Args:
        user_login: Login credentials
        db: Database session

    Returns:
        Token: Access and refresh tokens

    Raises:
        HTTPException: If credentials are invalid
    """
    # Authenticate user
    user = await UserService.authenticate_user(
        db,
        user_login.username,
        user_login.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Create tokens
    access_token = create_access_token(
        data={"sub": str(user.user_id), "username": user.username}
    )

    refresh_token = create_refresh_token(
        data={"sub": str(user.user_id), "username": user.username}
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )
