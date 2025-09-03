"""
AI API endpoints for LangChain integration.
Handles AI-powered operations like text generation and analysis.
"""

from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from backend.services.ai_service import AIService, AIError
from backend.config import get_settings


# Request/Response models
class AIGenerateRequest(BaseModel):
    """Request model for AI text generation."""
    
    prompt: str = Field(..., min_length=1, description="The prompt to send to the AI")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional context data")
    max_tokens: Optional[int] = Field(None, ge=1, le=4000, description="Maximum tokens to generate")


class AIAnalyzeRequest(BaseModel):
    """Request model for AI data analysis."""
    
    data: str = Field(..., min_length=1, description="Data to analyze")
    analysis_type: str = Field(default="summary", description="Type of analysis to perform")


class AIChatRequest(BaseModel):
    """Request model for AI chat completion."""
    
    messages: List[str] = Field(..., min_length=1, description="List of messages for chat")
    system_prompt: Optional[str] = Field(None, description="Optional system prompt")


class AIResponse(BaseModel):
    """Response model for AI operations."""
    
    content: str = Field(..., description="Generated or analyzed content")
    model_used: str = Field(..., description="AI model that was used")
    langsmith_enabled: bool = Field(..., description="Whether LangSmith tracing is enabled")


class AIStatusResponse(BaseModel):
    """Response model for AI service status."""
    
    service_available: bool = Field(..., description="Whether AI service is available")
    langsmith_status: Dict[str, Any] = Field(..., description="LangSmith integration status")
    configured_models: Dict[str, str] = Field(..., description="Configured AI models")


# Router for AI endpoints
router = APIRouter(prefix="/api/ai", tags=["ai"])


def get_ai_service() -> AIService:
    """Get AI service instance with current settings."""
    settings = get_settings()
    
    return AIService(
        openai_api_key=settings.openai_api_key,
        langsmith_api_key=settings.langsmith_api_key,
        langsmith_project=settings.langsmith_project,
        model_name=settings.default_content_model,
        temperature=settings.default_temperature
    )


@router.get("/status", response_model=AIStatusResponse)
async def get_ai_status():
    """
    Get AI service status and configuration.
    
    Returns information about AI service availability and LangSmith integration.
    """
    try:
        settings = get_settings()
        ai_service = get_ai_service()
        
        return AIStatusResponse(
            service_available=True,
            langsmith_status=ai_service.get_langsmith_status(),
            configured_models={
                "default_content_model": settings.default_content_model,
                "default_research_model": settings.default_research_model,
                "temperature": str(settings.default_temperature)
            }
        )
    except Exception as e:
        return AIStatusResponse(
            service_available=False,
            langsmith_status={"enabled": False, "error": str(e)},
            configured_models={}
        )


@router.post("/generate", response_model=AIResponse, status_code=status.HTTP_201_CREATED)
async def generate_ai_content(request: AIGenerateRequest):
    """
    Generate content using AI.
    
    This endpoint uses LangChain to generate text based on the provided prompt
    and optional context. LangSmith tracing is enabled if configured.
    """
    try:
        ai_service = get_ai_service()
        
        content = await ai_service.generate_text(
            prompt=request.prompt,
            context=request.context,
            max_tokens=request.max_tokens
        )
        
        settings = get_settings()
        return AIResponse(
            content=content,
            model_used=settings.default_content_model,
            langsmith_enabled=ai_service.langsmith_enabled
        )
        
    except AIError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI generation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred"
        )


@router.post("/analyze", response_model=AIResponse, status_code=status.HTTP_201_CREATED)
async def analyze_data(request: AIAnalyzeRequest):
    """
    Analyze data using AI.
    
    This endpoint uses AI to analyze provided data and return insights,
    summaries, or other analysis based on the specified type.
    """
    try:
        ai_service = get_ai_service()
        
        content = await ai_service.analyze_data(
            data=request.data,
            analysis_type=request.analysis_type
        )
        
        settings = get_settings()
        return AIResponse(
            content=content,
            model_used=settings.default_research_model,
            langsmith_enabled=ai_service.langsmith_enabled
        )
        
    except AIError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI analysis error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred"
        )


@router.post("/chat", response_model=AIResponse, status_code=status.HTTP_201_CREATED)
async def chat_completion(request: AIChatRequest):
    """
    Chat completion using AI.
    
    This endpoint provides chat completion functionality with multiple messages
    and optional system prompts.
    """
    try:
        ai_service = get_ai_service()
        
        content = await ai_service.chat_completion(
            messages=request.messages,
            system_prompt=request.system_prompt
        )
        
        settings = get_settings()
        return AIResponse(
            content=content,
            model_used=settings.default_content_model,
            langsmith_enabled=ai_service.langsmith_enabled
        )
        
    except AIError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat completion error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred"
        )
