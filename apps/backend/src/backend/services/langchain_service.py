"""
LangChain service for AI-powered content generation.
Integrates with OpenRouter for LLM access and LangSmith for observability.
"""

import time
import asyncio
import httpx
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, validator
from enum import Enum

from backend.models.client import ClientProfile


# Custom exceptions
class LangChainError(Exception):
    """Base exception for LangChain service errors."""
    pass


class OpenRouterError(Exception):
    """Exception for OpenRouter API errors."""
    pass


# Request/Response models
class ContentGenerationRequest(BaseModel):
    """Request model for content generation."""
    
    client_profile: ClientProfile = Field(
        ...,
        description="Client profile with context for content generation"
    )
    content_type: str = Field(
        ...,
        min_length=1,
        description="Type of content to generate (linkedin_post, newsletter, etc.)"
    )
    prompt: str = Field(
        ...,
        min_length=1,
        description="Main prompt for content generation"
    )
    context: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional context for content generation"
    )
    model: Optional[str] = Field(
        None,
        description="Specific model to use (overrides default)"
    )
    
    @validator('content_type')
    def validate_content_type(cls, v):
        """Validate content type is not empty."""
        if not v.strip():
            raise ValueError("Content type cannot be empty")
        return v.strip()
    
    @validator('prompt')
    def validate_prompt(cls, v):
        """Validate prompt is not empty."""
        if not v.strip():
            raise ValueError("Prompt cannot be empty")
        return v.strip()


class ContentGenerationResponse(BaseModel):
    """Response model for content generation."""
    
    content: str = Field(
        ...,
        description="Generated content"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata about the generation process"
    )
    quality_score: float = Field(
        0.0,
        ge=0.0,
        le=10.0,
        description="Quality score of generated content (0-10)"
    )
    processing_time: float = Field(
        0.0,
        ge=0.0,
        description="Processing time in seconds"
    )
    
    @validator('quality_score')
    def validate_quality_score(cls, v):
        """Validate quality score is within range."""
        if not (0.0 <= v <= 10.0):
            raise ValueError("Quality score must be between 0.0 and 10.0")
        return v


class LangChainService:
    """
    Service for AI-powered content generation using LangChain and OpenRouter.
    """
    
    def __init__(
        self,
        openrouter_api_key: str,
        langsmith_api_key: str,
        default_model: str = "openai/gpt-4"
    ):
        """
        Initialize LangChain service.
        
        Args:
            openrouter_api_key: API key for OpenRouter
            langsmith_api_key: API key for LangSmith tracing
            default_model: Default model to use for generation
        """
        if not openrouter_api_key or not openrouter_api_key.strip():
            raise ValueError("OpenRouter API key is required")
        
        if not langsmith_api_key or not langsmith_api_key.strip():
            raise ValueError("LangSmith API key is required")
        
        self.openrouter_api_key = openrouter_api_key.strip()
        self.langsmith_api_key = langsmith_api_key.strip()
        self.default_model = default_model
        
        # OpenRouter API configuration
        self.openrouter_base_url = "https://openrouter.ai/api/v1"
        self.openrouter_headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://phoenix-content-pipeline.com",
            "X-Title": "AI Content Pipeline"
        }
    
    async def generate_content(self, request: ContentGenerationRequest) -> ContentGenerationResponse:
        """
        Generate content using LangChain and OpenRouter.
        
        Args:
            request: Content generation request
            
        Returns:
            Generated content response
            
        Raises:
            LangChainError: If content generation fails
        """
        start_time = time.time()
        
        try:
            # Build prompts with client context
            system_prompt = self._build_system_prompt(request.client_profile)
            user_prompt = self._build_user_prompt(request.prompt, request.context)
            
            # Call OpenRouter API
            model = request.model or self.default_model
            api_response = await self._call_openrouter(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=model
            )
            
            # Extract content from response
            content = self._extract_content_from_response(api_response)
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(content, request.client_profile)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Build response
            response = ContentGenerationResponse(
                content=content,
                metadata={
                    "model": model,
                    "tokens_used": api_response.get("usage", {}).get("total_tokens", 0),
                    "cost": self._estimate_cost(api_response.get("usage", {}), model),
                    "system_prompt_length": len(system_prompt),
                    "user_prompt_length": len(user_prompt)
                },
                quality_score=quality_score,
                processing_time=processing_time
            )
            
            return response
            
        except OpenRouterError as e:
            raise LangChainError(f"OpenRouter API error: {str(e)}")
        
        except ConnectionError as e:
            raise LangChainError(f"Connection error: {str(e)}")
        
        except TimeoutError as e:
            raise LangChainError(f"Request timed out: {str(e)}")
        
        except Exception as e:
            raise LangChainError(f"Unexpected error during content generation: {str(e)}")
    
    def _build_system_prompt(self, client_profile: ClientProfile) -> str:
        """
        Build system prompt with client context.
        
        Args:
            client_profile: Client profile for context
            
        Returns:
            System prompt string
        """
        # Extract client context
        industry = client_profile.icp_profile.industry
        services = ", ".join(client_profile.service_offering.services)
        positioning = client_profile.positioning_statement
        platforms = ", ".join(client_profile.content_preferences.platforms)
        content_types = ", ".join(client_profile.content_preferences.content_types)
        tone = client_profile.content_preferences.tone or "professional"
        
        system_prompt = f"""You are an expert content strategist and copywriter specializing in {industry} companies.

Client Context:
- Industry: {industry}
- Services: {services}
- Positioning: {positioning}
- Preferred Platforms: {platforms}
- Content Types: {content_types}
- Tone: {tone}

Your role is to create high-quality, engaging content that:
1. Aligns with the client's positioning and expertise
2. Resonates with their target audience in the {industry} industry
3. Maintains the specified tone: {tone}
4. Follows best practices for the target platform
5. Provides genuine value and insights

Always ensure content is:
- Authentic and reflects the client's expertise
- Relevant to their target audience's pain points
- Actionable and valuable
- Appropriately formatted for the platform
- Free of generic marketing speak
"""
        
        return system_prompt
    
    def _build_user_prompt(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Build user prompt with additional context.
        
        Args:
            prompt: Base prompt
            context: Additional context dictionary
            
        Returns:
            Enhanced user prompt
        """
        if not context:
            return prompt
        
        context_parts = []
        for key, value in context.items():
            if value:
                context_parts.append(f"{key.replace('_', ' ').title()}: {value}")
        
        if context_parts:
            context_string = "\n".join(context_parts)
            return f"{prompt}\n\nAdditional Context:\n{context_string}"
        
        return prompt
    
    async def _call_openrouter(
        self,
        messages: list,
        model: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Make API call to OpenRouter.
        
        Args:
            messages: List of message objects
            model: Model to use
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation
            
        Returns:
            API response dictionary
            
        Raises:
            OpenRouterError: If API call fails
        """
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.openrouter_base_url}/chat/completions",
                    headers=self.openrouter_headers,
                    json=payload
                )
                
                if response.status_code != 200:
                    error_detail = response.text
                    raise OpenRouterError(
                        f"OpenRouter API returned status {response.status_code}: {error_detail}"
                    )
                
                return response.json()
                
        except httpx.TimeoutException:
            raise TimeoutError("OpenRouter API request timed out")
        
        except httpx.ConnectError:
            raise ConnectionError("Failed to connect to OpenRouter API")
        
        except Exception as e:
            if isinstance(e, (OpenRouterError, TimeoutError, ConnectionError)):
                raise
            raise OpenRouterError(f"Unexpected error calling OpenRouter API: {str(e)}")
    
    def _extract_content_from_response(self, response: Dict[str, Any]) -> str:
        """
        Extract content from OpenRouter API response.
        
        Args:
            response: API response dictionary
            
        Returns:
            Generated content string
            
        Raises:
            LangChainError: If response format is invalid
        """
        try:
            choices = response.get("choices", [])
            if not choices:
                raise LangChainError("Invalid response format: no choices found")
            
            message = choices[0].get("message", {})
            content = message.get("content", "").strip()
            
            if not content:
                raise LangChainError("Invalid response format: empty content")
            
            return content
            
        except (KeyError, IndexError, TypeError) as e:
            raise LangChainError(f"Invalid response format: {str(e)}")
    
    def _calculate_quality_score(self, content: str, client_profile: ClientProfile) -> float:
        """
        Calculate quality score for generated content.
        
        Args:
            content: Generated content
            client_profile: Client profile for context
            
        Returns:
            Quality score (0.0-10.0)
        """
        score = 5.0  # Base score
        
        # Length scoring
        if len(content) < 50:
            score -= 2.0  # Too short
        elif len(content) > 2000:
            score -= 1.0  # Too long
        elif 100 <= len(content) <= 1000:
            score += 1.0  # Good length
        
        # Relevance scoring (basic keyword matching)
        content_lower = content.lower()
        
        # Check for industry relevance
        if client_profile.icp_profile.industry.lower() in content_lower:
            score += 1.0
        
        # Check for service relevance
        services = [s.lower() for s in client_profile.service_offering.services]
        if any(service in content_lower for service in services):
            score += 1.0
        
        # Check for positioning relevance
        positioning_words = client_profile.positioning_statement.lower().split()
        key_words = [word for word in positioning_words if len(word) > 4]
        if any(word in content_lower for word in key_words[:3]):
            score += 0.5
        
        # Basic quality indicators
        if "." in content:  # Has sentences
            score += 0.5
        
        if content.count("\n") >= 2:  # Has structure
            score += 0.5
        
        # Ensure score is within bounds
        return max(0.0, min(10.0, score))
    
    def _estimate_cost(self, usage: Dict[str, Any], model: str) -> float:
        """
        Estimate cost of API call based on usage and model.
        
        Args:
            usage: Usage statistics from API response
            model: Model used
            
        Returns:
            Estimated cost in USD
        """
        # Simplified cost estimation (would need real pricing data)
        tokens = usage.get("total_tokens", 0)
        
        # Basic cost estimates (per 1K tokens)
        cost_per_1k = {
            "openai/gpt-4": 0.03,
            "openai/gpt-3.5-turbo": 0.002,
            "anthropic/claude-3-haiku": 0.00025,
            "anthropic/claude-3-sonnet": 0.003,
        }
        
        rate = cost_per_1k.get(model, 0.01)  # Default rate
        return (tokens / 1000) * rate
