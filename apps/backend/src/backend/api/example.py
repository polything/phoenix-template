"""
Example API endpoints for the Phoenix Template.
Handles basic CRUD operations for demonstration purposes.
"""

from typing import List
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, HTTPException, status

from backend.models.example import (
    ExampleItem,
    ExampleItemCreate,
    ExampleItemUpdate,
    ExampleItemResponse
)

# Router for example endpoints
router = APIRouter(prefix="/api/example", tags=["example"])

# In-memory storage for demonstration (replace with database in real implementation)
example_items: List[ExampleItem] = []


@router.post("/items", response_model=ExampleItemResponse, status_code=status.HTTP_201_CREATED)
async def create_example_item(item_data: ExampleItemCreate):
    """
    Create a new example item.
    
    This endpoint:
    1. Validates the input data
    2. Creates a new example item
    3. Stores it (in-memory for demo)
    4. Returns the created item
    """
    try:
        # Create new item
        new_item = ExampleItem(
            name=item_data.name,
            description=item_data.description,
            email=item_data.email
        )
        
        # Store item (in-memory for demo)
        example_items.append(new_item)
        
        # Return response
        return ExampleItemResponse.from_example_item(new_item)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred"
        )


@router.get("/items", response_model=List[ExampleItemResponse])
async def get_example_items():
    """
    Get all example items.
    
    Returns a list of all example items.
    """
    try:
        return [ExampleItemResponse.from_example_item(item) for item in example_items]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred"
        )


@router.get("/items/{item_id}", response_model=ExampleItemResponse)
async def get_example_item(item_id: UUID):
    """
    Get a specific example item by ID.
    
    Returns the example item with the specified ID.
    """
    try:
        # Find item by ID
        item = next((item for item in example_items if item.id == item_id), None)
        
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Example item not found"
            )
        
        return ExampleItemResponse.from_example_item(item)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred"
        )


@router.put("/items/{item_id}", response_model=ExampleItemResponse)
async def update_example_item(item_id: UUID, update_data: ExampleItemUpdate):
    """
    Update an example item.
    
    Allows partial updates to item information. Only provided fields
    will be updated, others will remain unchanged.
    """
    try:
        # Find item by ID
        item_index = next((i for i, item in enumerate(example_items) if item.id == item_id), None)
        
        if item_index is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Example item not found"
            )
        
        # Update item with provided data
        item = example_items[item_index]
        update_dict = update_data.model_dump(exclude_unset=True)
        
        for field, value in update_dict.items():
            setattr(item, field, value)
        
        # Update timestamp
        item.updated_at = datetime.now()
        
        return ExampleItemResponse.from_example_item(item)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred"
        )


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_example_item(item_id: UUID):
    """
    Delete an example item.
    
    This will permanently remove the item.
    """
    try:
        # Find item by ID
        item_index = next((i for i, item in enumerate(example_items) if item.id == item_id), None)
        
        if item_index is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Example item not found"
            )
        
        # Remove item
        example_items.pop(item_index)
        
        return None  # 204 No Content
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred"
        )
