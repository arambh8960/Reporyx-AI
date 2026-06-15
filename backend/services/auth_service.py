"""
Authentication Service
Handles user authentication business logic
"""

from typing import Optional, Dict
from bson import ObjectId
from datetime import datetime

from database.mongo_db import get_collection
from models.user_model import UserCreate, UserLogin
from utils.password import hash_password, verify_password
from services.jwt_service import create_access_token


async def create_user(user_data: UserCreate) -> Dict:
    """
    Create a new user in the database
    
    Args:
        user_data: User creation data
        
    Returns:
        Created user document
        
    Raises:
        ValueError: If email already exists
    """
    users_collection = get_collection("users")
    
    # Check if user with email already exists
    existing_user = await users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise ValueError("Email already registered")
    
    # Hash password
    password_hash = hash_password(user_data.password)
    
    # Create user document
    user_document = {
        "name": user_data.name,
        "email": user_data.email,
        "password_hash": password_hash,
        "created_at": datetime.utcnow()
    }
    
    # Insert user into database
    result = await users_collection.insert_one(user_document)
    
    # Return created user
    created_user = await users_collection.find_one({"_id": result.inserted_id})
    return created_user


async def authenticate_user(user_data: UserLogin) -> Optional[Dict]:
    """
    Authenticate a user with email and password
    
    Args:
        user_data: User login data
        
    Returns:
        User document if authentication successful, None otherwise
    """
    users_collection = get_collection("users")
    
    # Find user by email
    user = await users_collection.find_one({"email": user_data.email})
    
    if not user:
        return None
    
    # Verify password
    if not verify_password(user_data.password, user["password_hash"]):
        return None
    
    return user


async def login_user(user_data: UserLogin) -> Optional[Dict]:
    """
    Login a user and generate JWT token
    
    Args:
        user_data: User login data
        
    Returns:
        Dictionary with access_token and token_type if successful, None otherwise
    """
    # Authenticate user
    user = await authenticate_user(user_data)
    
    if not user:
        return None
    
    # Create JWT token
    token_data = {"sub": str(user["_id"]), "email": user["email"]}
    access_token = create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


async def get_user_by_id(user_id: str) -> Optional[Dict]:
    """
    Get a user by ID
    
    Args:
        user_id: User ID as string
        
    Returns:
        User document if found, None otherwise
    """
    users_collection = get_collection("users")
    
    try:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        return user
    except:
        return None


async def get_user_by_email(email: str) -> Optional[Dict]:
    """
    Get a user by email
    
    Args:
        email: User email
        
    Returns:
        User document if found, None otherwise
    """
    users_collection = get_collection("users")
    user = await users_collection.find_one({"email": email})
    return user
