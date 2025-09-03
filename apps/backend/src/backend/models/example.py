"""
Example data models for the Phoenix Template.
Defines basic Pydantic models for demonstration purposes.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class ExampleItem(BaseModel):
    """Model for example items."""
    
    id: Optional[UUID] = Field(
        default_factory=uuid4,
        description="Unique item identifier"
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Item name"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Item description"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Contact email"
    )
    is_active: bool = Field(
        default=True,
        description="Whether the item is active"
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="When the item was created"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="When the item was last updated"
    )
    
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat(),
            UUID: str
        }
    )


class ExampleItemCreate(BaseModel):
    """Model for creating example items."""
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Item name"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Item description"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Contact email"
    )


class ExampleItemUpdate(BaseModel):
    """Model for updating example items (partial updates allowed)."""
    
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Item name"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Item description"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Contact email"
    )
    is_active: Optional[bool] = Field(
        None,
        description="Whether the item is active"
    )


class ExampleItemResponse(BaseModel):
    """Response model for example item API endpoints."""
    
    id: UUID
    name: str
    description: Optional[str]
    email: Optional[EmailStr]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat(),
            UUID: str
        }
    )
    
    @classmethod
    def from_example_item(cls, item: ExampleItem) -> "ExampleItemResponse":
        """Create response from example item."""
        return cls(
            id=item.id,
            name=item.name,
            description=item.description,
            email=item.email,
            is_active=item.is_active,
            created_at=item.created_at,
            updated_at=item.updated_at
        )
