"""
Health check API endpoints.
"""

from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    timestamp: datetime
    version: str


router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns the current status of the API, timestamp, and version.
    Used for monitoring and load balancer health checks.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )
