"""
Authentication Schemas
Pydantic schemas for authentication requests and responses
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class SignupRequest(BaseModel):
    """
    Schema for user signup request
    """
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, max_length=100, description="User's password (min 8 characters)")


class LoginRequest(BaseModel):
    """
    Schema for user login request
    """
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class SignupResponse(BaseModel):
    """
    Schema for signup response
    """
    message: str = Field(..., description="Success message")
    user_id: str = Field(..., description="ID of the created user")


class ErrorResponse(BaseModel):
    """
    Schema for error responses
    """
    detail: str = Field(..., description="Error message")
