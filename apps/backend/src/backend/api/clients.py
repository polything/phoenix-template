"""
Client API endpoints for the AI-Enhanced Autonomous Content Pipeline.
Handles client intake, CRUD operations, and client management.
"""

from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Query, Depends
from fastapi.responses import JSONResponse

from backend.models.client import (
    ClientIntakeRequest,
    ClientProfile,
    ClientProfileUpdate,
    ClientProfileResponse,
    ClientListResponse
)
from backend.services.database_service import (
    get_database_service,
    ClientNotFoundError,
    DuplicateEmailError,
    DatabaseError
)


# Get database service instance
db_service = get_database_service()


# Router for client endpoints
router = APIRouter(prefix="/api/clients", tags=["clients"])


# Service functions using database service
async def create_client_from_intake(intake_request: ClientIntakeRequest) -> ClientProfile:
    """
    Create a new client profile from intake request.
    """
    return await db_service.create_client(intake_request)


async def get_clients_list(
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None
) -> ClientListResponse:
    """
    Get paginated list of clients with optional search.
    """
    result = await db_service.get_clients_list(page=page, page_size=page_size, search=search)
    
    # Convert to response format
    client_responses = [
        ClientProfileResponse.from_client_profile(client) 
        for client in result["clients"]
    ]
    
    return ClientListResponse(
        clients=client_responses,
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"]
    )


async def get_client_by_id(client_id: UUID) -> ClientProfile:
    """
    Get client profile by ID.
    """
    return await db_service.get_client_by_id(client_id)


async def update_client(client_id: UUID, update_data: ClientProfileUpdate) -> ClientProfile:
    """
    Update client profile.
    """
    # Convert Pydantic model to dict, excluding None values
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
    return await db_service.update_client(client_id, update_dict)


async def delete_client(client_id: UUID) -> bool:
    """
    Delete client profile.
    """
    return await db_service.delete_client(client_id)


# API Endpoints
@router.post("/intake", response_model=ClientProfile, status_code=status.HTTP_201_CREATED)
async def create_client_intake(intake_request: ClientIntakeRequest):
    """
    Create a new client from intake form submission.
    
    This endpoint:
    1. Validates the intake request
    2. Checks for duplicate email addresses
    3. Creates a new client profile
    4. Stores it in the database
    5. Returns the created client profile
    """
    try:
        client_profile = await create_client_from_intake(intake_request)
        return client_profile
    
    except DuplicateEmailError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    except Exception as e:
        # Log the error in production
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred"
        )


@router.get("", response_model=ClientListResponse)
async def get_clients(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    search: Optional[str] = Query(None, description="Search term for filtering clients")
):
    """
    Get a paginated list of clients with optional search functionality.
    
    Query parameters:
    - page: Page number (starting from 1)
    - page_size: Number of items per page (1-100)
    - search: Optional search term to filter clients by name, email, or company
    """
    try:
        clients = await get_clients_list(page=page, page_size=page_size, search=search)
        return clients
    
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    except Exception as e:
        # Log the error in production
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred"
        )


@router.get("/{client_id}", response_model=ClientProfile)
async def get_client(client_id: UUID):
    """
    Get a specific client profile by ID.
    
    Returns the complete client profile including all intake data,
    preferences, constraints, and metadata.
    """
    try:
        client_profile = await get_client_by_id(client_id)
        return client_profile
    
    except ClientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    except Exception as e:
        # Log the error in production
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred"
        )


@router.put("/{client_id}", response_model=ClientProfile)
async def update_client_profile(client_id: UUID, update_data: ClientProfileUpdate):
    """
    Update a client profile.
    
    Allows partial updates to client information. Only provided fields
    will be updated, others will remain unchanged.
    """
    try:
        updated_client = await update_client(client_id, update_data)
        return updated_client
    
    except ClientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    except Exception as e:
        # Log the error in production
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred"
        )


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client_profile(client_id: UUID):
    """
    Delete a client profile.
    
    This will permanently remove the client and all associated data
    including pipeline runs, content, and performance metrics.
    """
    try:
        await delete_client(client_id)
        return None  # 204 No Content
    
    except ClientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    except Exception as e:
        # Log the error in production
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred"
        )
