"""
Health Check Routes
Endpoint for checking backend health status
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    
    Returns:
        JSON response with backend status
    """
    return {
        "status": "success",
        "message": "Backend Connected"
    }
