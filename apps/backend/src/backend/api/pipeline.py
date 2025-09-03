"""
Content Pipeline API endpoints for the AI-Enhanced Autonomous Content Pipeline.
Handles content generation requests and pipeline execution.
"""

from typing import Dict, Any, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field

from backend.models.client import ClientProfile
from backend.services.database_service import get_database_service, DatabaseError
from backend.services.langchain_service import (
    LangChainService,
    ContentGenerationRequest,
    ContentGenerationResponse,
    LangChainError
)
from backend.config import get_settings


# Request/Response models
class PipelineRequest(BaseModel):
    """Request model for content pipeline execution."""
    
    client_id: UUID = Field(..., description="Client ID for content generation")
    content_type: str = Field(..., min_length=1, description="Type of content to generate")
    prompt: str = Field(..., min_length=1, description="Main prompt for content generation")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")
    model: Optional[str] = Field(None, description="Specific model to use")


class PipelineResponse(BaseModel):
    """Response model for content pipeline execution."""
    
    pipeline_run_id: UUID = Field(..., description="Pipeline run ID")
    content: str = Field(..., description="Generated content")
    quality_score: float = Field(..., description="Quality score (0-10)")
    processing_time: float = Field(..., description="Processing time in seconds")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Generation metadata")


# Router for pipeline endpoints
router = APIRouter(prefix="/api/pipeline", tags=["pipeline"])

# Get service instances
db_service = get_database_service()
settings = get_settings()


def get_langchain_service() -> LangChainService:
    """Get LangChain service instance."""
    return LangChainService(
        openrouter_api_key=settings.openrouter_api_key,
        langsmith_api_key=settings.langsmith_api_key,
        default_model=settings.default_content_model
    )


@router.post("/generate", response_model=PipelineResponse, status_code=status.HTTP_201_CREATED)
async def generate_content(request: PipelineRequest):
    """
    Generate content using the AI pipeline.
    
    This endpoint:
    1. Retrieves the client profile from the database
    2. Creates a pipeline run record
    3. Executes the LangChain content generation
    4. Updates the pipeline run with results
    5. Returns the generated content and metadata
    """
    try:
        # Get client profile
        client_profile = await db_service.get_client_by_id(request.client_id)
        
        # Create pipeline run
        pipeline_run_id = await db_service.create_pipeline_run(
            client_id=request.client_id,
            input_data={
                "content_type": request.content_type,
                "prompt": request.prompt,
                "context": request.context,
                "model": request.model
            },
            stage="content_generation"
        )
        
        # Initialize LangChain service
        langchain_service = get_langchain_service()
        
        # Create content generation request
        generation_request = ContentGenerationRequest(
            client_profile=client_profile,
            content_type=request.content_type,
            prompt=request.prompt,
            context=request.context,
            model=request.model
        )
        
        # Generate content
        generation_response = await langchain_service.generate_content(generation_request)
        
        # Update pipeline run with results
        await db_service.update_pipeline_run(
            run_id=pipeline_run_id,
            updates={
                "status": "completed",
                "stage": "content_generation",
                "draft_content": {
                    "content": generation_response.content,
                    "quality_score": generation_response.quality_score,
                    "metadata": generation_response.metadata
                },
                "quality_score": generation_response.quality_score,
                "processing_time_seconds": int(generation_response.processing_time),
                "ai_model_calls": {
                    "model": generation_response.metadata.get("model"),
                    "tokens_used": generation_response.metadata.get("tokens_used", 0),
                    "cost": generation_response.metadata.get("cost", 0.0)
                },
                "completed_at": "now()"
            }
        )
        
        # Return response
        return PipelineResponse(
            pipeline_run_id=pipeline_run_id,
            content=generation_response.content,
            quality_score=generation_response.quality_score,
            processing_time=generation_response.processing_time,
            metadata=generation_response.metadata
        )
        
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    except LangChainError as e:
        # Update pipeline run with error status
        if 'pipeline_run_id' in locals():
            await db_service.update_pipeline_run(
                run_id=pipeline_run_id,
                updates={
                    "status": "failed",
                    "error_message": str(e),
                    "completed_at": "now()"
                }
            )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Content generation error: {str(e)}"
        )
    
    except Exception as e:
        # Update pipeline run with error status
        if 'pipeline_run_id' in locals():
            await db_service.update_pipeline_run(
                run_id=pipeline_run_id,
                updates={
                    "status": "failed",
                    "error_message": str(e),
                    "completed_at": "now()"
                }
            )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred"
        )


@router.get("/runs/{run_id}")
async def get_pipeline_run(run_id: UUID):
    """
    Get pipeline run details by ID.
    
    Returns the complete pipeline run information including
    input data, stage outputs, and metadata.
    """
    try:
        # This would query the database for pipeline run details
        # For now, return a placeholder response
        return {
            "id": run_id,
            "status": "completed",
            "message": "Pipeline run details endpoint - to be implemented"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred"
        )


@router.get("/clients/{client_id}/runs")
async def get_client_pipeline_runs(
    client_id: UUID,
    limit: int = 10,
    offset: int = 0
):
    """
    Get pipeline runs for a specific client.
    
    Returns a list of pipeline runs with pagination.
    """
    try:
        # This would query the database for client pipeline runs
        # For now, return a placeholder response
        return {
            "client_id": client_id,
            "runs": [],
            "total": 0,
            "limit": limit,
            "offset": offset,
            "message": "Client pipeline runs endpoint - to be implemented"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred"
        )
