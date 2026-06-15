"""
Authentication Routes
Endpoints for user signup and login
"""

from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from schemas.auth_schema import SignupRequest, LoginRequest, SignupResponse, ErrorResponse
from schemas.token_schema import Token
from services.auth_service import create_user, login_user
from models.user_model import UserCreate, UserLogin


router = APIRouter()


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: SignupRequest):
    """
    User signup endpoint
    
    Args:
        user_data: User signup data (name, email, password)
        
    Returns:
        Signup response with success message and user ID
        
    Raises:
        HTTPException: If email already exists or validation fails
    """
    try:
        # Convert to user model
        user_create = UserCreate(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password
        )
        
        # Create user
        created_user = await create_user(user_create)
        
        return SignupResponse(
            message="User created successfully",
            user_id=str(created_user["_id"])
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during signup: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(user_data: LoginRequest):
    """
    User login endpoint
    
    Args:
        user_data: User login data (email, password)
        
    Returns:
        JWT access token
        
    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        # Convert to user model
        user_login = UserLogin(
            email=user_data.email,
            password=user_data.password
        )
        
        # Login user
        token_data = await login_user(user_login)
        
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return Token(
            access_token=token_data["access_token"],
            token_type=token_data["token_type"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during login: {str(e)}"
        )
