"""
Token Schemas
Pydantic schemas for JWT token responses
"""

from pydantic import BaseModel, Field


class Token(BaseModel):
    """
    Schema for JWT token response
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
