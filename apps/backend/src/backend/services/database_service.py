"""
Database service for Supabase integration.
Handles all database operations for the AI-Enhanced Autonomous Content Pipeline.
"""

import asyncio
from typing import List, Optional, Dict, Any, Union
from uuid import UUID
import json
from datetime import datetime

from supabase import create_client, Client
from pydantic import BaseModel

from backend.config import get_settings
from backend.models.client import ClientProfile, ClientIntakeRequest
from backend.services.langchain_service import ContentGenerationRequest, ContentGenerationResponse


class DatabaseError(Exception):
    """Base exception for database operations."""
    pass


class ClientNotFoundError(DatabaseError):
    """Raised when a client is not found."""
    pass


class DuplicateEmailError(DatabaseError):
    """Raised when trying to create a client with an existing email."""
    pass


class DatabaseService:
    """
    Service for database operations using Supabase.
    """
    
    def __init__(self):
        """Initialize database service with Supabase client."""
        settings = get_settings()
        
        self.supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
        
        # Use service role key if available for admin operations
        if settings.supabase_service_role_key:
            self.admin_supabase: Client = create_client(
                settings.supabase_url,
                settings.supabase_service_role_key
            )
        else:
            self.admin_supabase = self.supabase
    
    async def create_client(self, intake_request: ClientIntakeRequest) -> ClientProfile:
        """
        Create a new client from intake request.
        
        Args:
            intake_request: Client intake form data
            
        Returns:
            Created client profile
            
        Raises:
            DuplicateEmailError: If email already exists
            DatabaseError: If database operation fails
        """
        try:
            # Check for duplicate email
            existing_client = await self.get_client_by_email(intake_request.email)
            if existing_client:
                raise DuplicateEmailError(f"Client with email {intake_request.email} already exists")
            
            # Convert intake request to client profile
            client_profile = ClientProfile.from_intake_request(intake_request)
            
            # Prepare data for database insertion
            client_data = {
                "name": client_profile.name,
                "email": client_profile.email,
                "company": client_profile.company,
                "website": str(client_profile.website) if client_profile.website else None,
                "service_offering": client_profile.service_offering.model_dump(),
                "icp_profile": client_profile.icp_profile.model_dump(),
                "positioning_statement": client_profile.positioning_statement,
                "content_preferences": client_profile.content_preferences.model_dump(),
                "constraints": client_profile.constraints.model_dump() if client_profile.constraints else None,
                "voice_examples": [example.model_dump() for example in client_profile.voice_examples] if client_profile.voice_examples else None,
                "proof_assets": [asset.model_dump() for asset in client_profile.proof_assets] if client_profile.proof_assets else None,
                "additional_notes": client_profile.additional_notes,
                "status": client_profile.status.value,
                "created_at": client_profile.created_at.isoformat() if client_profile.created_at else None,
                "updated_at": client_profile.updated_at.isoformat() if client_profile.updated_at else None
            }
            
            # Insert into database
            result = self.supabase.table("clients").insert(client_data).execute()
            
            if not result.data:
                raise DatabaseError("Failed to create client - no data returned")
            
            # Get the created client with ID
            created_data = result.data[0]
            client_profile.id = UUID(created_data["id"])
            client_profile.created_at = datetime.fromisoformat(created_data["created_at"].replace('Z', '+00:00'))
            client_profile.updated_at = datetime.fromisoformat(created_data["updated_at"].replace('Z', '+00:00'))
            
            return client_profile
            
        except DuplicateEmailError:
            raise
        except Exception as e:
            if isinstance(e, DatabaseError):
                raise
            raise DatabaseError(f"Failed to create client: {str(e)}")
    
    async def get_client_by_id(self, client_id: UUID) -> ClientProfile:
        """
        Get client profile by ID.
        
        Args:
            client_id: Client UUID
            
        Returns:
            Client profile
            
        Raises:
            ClientNotFoundError: If client not found
            DatabaseError: If database operation fails
        """
        try:
            result = self.supabase.table("clients").select("*").eq("id", str(client_id)).execute()
            
            if not result.data:
                raise ClientNotFoundError(f"Client with ID {client_id} not found")
            
            client_data = result.data[0]
            return self._convert_db_row_to_client_profile(client_data)
            
        except ClientNotFoundError:
            raise
        except Exception as e:
            if isinstance(e, DatabaseError):
                raise
            raise DatabaseError(f"Failed to get client by ID: {str(e)}")
    
    async def get_client_by_email(self, email: str) -> Optional[ClientProfile]:
        """
        Get client profile by email.
        
        Args:
            email: Client email address
            
        Returns:
            Client profile or None if not found
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            result = self.supabase.table("clients").select("*").eq("email", email).execute()
            
            if not result.data:
                return None
            
            client_data = result.data[0]
            return self._convert_db_row_to_client_profile(client_data)
            
        except Exception as e:
            raise DatabaseError(f"Failed to get client by email: {str(e)}")
    
    async def get_clients_list(
        self,
        page: int = 1,
        page_size: int = 10,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get paginated list of clients with optional search.
        
        Args:
            page: Page number (1-based)
            page_size: Number of items per page
            search: Optional search term
            
        Returns:
            Dictionary with clients list and pagination info
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            # Calculate offset
            offset = (page - 1) * page_size
            
            # Build query
            query = self.supabase.table("clients").select("*", count="exact")
            
            # Add search filter if provided
            if search:
                query = query.or_(f"name.ilike.%{search}%,email.ilike.%{search}%,company.ilike.%{search}%")
            
            # Add pagination
            query = query.range(offset, offset + page_size - 1)
            
            # Execute query
            result = query.execute()
            
            # Convert to client profiles
            clients = [self._convert_db_row_to_client_profile(row) for row in result.data]
            
            return {
                "clients": clients,
                "total": result.count or 0,
                "page": page,
                "page_size": page_size
            }
            
        except Exception as e:
            raise DatabaseError(f"Failed to get clients list: {str(e)}")
    
    async def update_client(self, client_id: UUID, update_data: Dict[str, Any]) -> ClientProfile:
        """
        Update client profile.
        
        Args:
            client_id: Client UUID
            update_data: Dictionary of fields to update
            
        Returns:
            Updated client profile
            
        Raises:
            ClientNotFoundError: If client not found
            DatabaseError: If database operation fails
        """
        try:
            # Add updated_at timestamp
            update_data["updated_at"] = datetime.now().isoformat()
            
            # Update in database
            result = self.supabase.table("clients").update(update_data).eq("id", str(client_id)).execute()
            
            if not result.data:
                raise ClientNotFoundError(f"Client with ID {client_id} not found")
            
            client_data = result.data[0]
            return self._convert_db_row_to_client_profile(client_data)
            
        except ClientNotFoundError:
            raise
        except Exception as e:
            if isinstance(e, DatabaseError):
                raise
            raise DatabaseError(f"Failed to update client: {str(e)}")
    
    async def delete_client(self, client_id: UUID) -> bool:
        """
        Delete client profile.
        
        Args:
            client_id: Client UUID
            
        Returns:
            True if deleted successfully
            
        Raises:
            ClientNotFoundError: If client not found
            DatabaseError: If database operation fails
        """
        try:
            result = self.supabase.table("clients").delete().eq("id", str(client_id)).execute()
            
            if not result.data:
                raise ClientNotFoundError(f"Client with ID {client_id} not found")
            
            return True
            
        except ClientNotFoundError:
            raise
        except Exception as e:
            if isinstance(e, DatabaseError):
                raise
            raise DatabaseError(f"Failed to delete client: {str(e)}")
    
    async def create_pipeline_run(
        self,
        client_id: UUID,
        input_data: Dict[str, Any],
        stage: str = "pending"
    ) -> UUID:
        """
        Create a new content pipeline run.
        
        Args:
            client_id: Client UUID
            input_data: Input data for the pipeline
            stage: Initial stage
            
        Returns:
            Pipeline run UUID
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            pipeline_data = {
                "client_id": str(client_id),
                "status": "pending",
                "stage": stage,
                "input_data": input_data,
                "created_at": datetime.now().isoformat()
            }
            
            result = self.supabase.table("content_pipeline_runs").insert(pipeline_data).execute()
            
            if not result.data:
                raise DatabaseError("Failed to create pipeline run - no data returned")
            
            return UUID(result.data[0]["id"])
            
        except Exception as e:
            if isinstance(e, DatabaseError):
                raise
            raise DatabaseError(f"Failed to create pipeline run: {str(e)}")
    
    async def update_pipeline_run(
        self,
        run_id: UUID,
        updates: Dict[str, Any]
    ) -> bool:
        """
        Update a content pipeline run.
        
        Args:
            run_id: Pipeline run UUID
            updates: Dictionary of fields to update
            
        Returns:
            True if updated successfully
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            result = self.supabase.table("content_pipeline_runs").update(updates).eq("id", str(run_id)).execute()
            
            return bool(result.data)
            
        except Exception as e:
            raise DatabaseError(f"Failed to update pipeline run: {str(e)}")
    
    def _convert_db_row_to_client_profile(self, row: Dict[str, Any]) -> ClientProfile:
        """
        Convert database row to ClientProfile object.
        
        Args:
            row: Database row data
            
        Returns:
            ClientProfile object
        """
        # Handle JSON fields
        service_offering = row.get("service_offering", {})
        icp_profile = row.get("icp_profile", {})
        content_preferences = row.get("content_preferences", {})
        constraints = row.get("constraints", {})
        voice_examples = row.get("voice_examples", [])
        proof_assets = row.get("proof_assets", [])
        
        # Convert datetime strings
        created_at = None
        updated_at = None
        
        if row.get("created_at"):
            created_at = datetime.fromisoformat(row["created_at"].replace('Z', '+00:00'))
        
        if row.get("updated_at"):
            updated_at = datetime.fromisoformat(row["updated_at"].replace('Z', '+00:00'))
        
        return ClientProfile(
            id=UUID(row["id"]),
            name=row["name"],
            email=row["email"],
            company=row.get("company"),
            website=row.get("website"),
            service_offering=service_offering,
            icp_profile=icp_profile,
            positioning_statement=row["positioning_statement"],
            content_preferences=content_preferences,
            constraints=constraints if constraints else None,
            voice_examples=voice_examples if voice_examples else [],
            proof_assets=proof_assets if proof_assets else [],
            additional_notes=row.get("additional_notes"),
            status=row.get("status", "active"),
            created_at=created_at,
            updated_at=updated_at
        )


# Global database service instance
db_service = DatabaseService()


def get_database_service() -> DatabaseService:
    """Get database service instance."""
    return db_service
