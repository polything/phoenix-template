"""
Test cases for LangChain service integration.
Following TDD methodology - these tests define the expected AI service behavior.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any

from backend.services.langchain_service import (
    LangChainService,
    ContentGenerationRequest,
    ContentGenerationResponse,
    LangChainError,
    OpenRouterError
)
from backend.models.client import ClientProfile


@pytest.fixture
def sample_client_profile():
    """Sample client profile for testing."""
    return ClientProfile(
        name="Test Client",
        email="test@example.com",
        service_offering={
            "services": ["Content Strategy"],
            "pricing_tier": "premium"
        },
        icp_profile={
            "industry": "SaaS",
            "company_size": "10-50",
            "pain_points": ["Low engagement"]
        },
        positioning_statement="We help SaaS companies build thought leadership.",
        content_preferences={
            "platforms": ["linkedin"],
            "frequency": "weekly",
            "content_types": ["educational"]
        }
    )


@pytest.fixture
def langchain_service():
    """Create LangChain service instance for testing."""
    return LangChainService(
        openrouter_api_key="test-api-key",
        langsmith_api_key="test-langsmith-key"
    )


class TestLangChainServiceInitialization:
    """Test cases for LangChain service initialization."""
    
    def test_service_initialization_success(self):
        """Test successful service initialization with API keys."""
        service = LangChainService(
            openrouter_api_key="test-key",
            langsmith_api_key="langsmith-key"
        )
        
        assert service.openrouter_api_key == "test-key"
        assert service.langsmith_api_key == "langsmith-key"
        assert service.default_model == "openai/gpt-4"
    
    def test_service_initialization_missing_keys(self):
        """Test service initialization with missing API keys."""
        with pytest.raises(ValueError, match="OpenRouter API key is required"):
            LangChainService(openrouter_api_key="", langsmith_api_key="test")
        
        with pytest.raises(ValueError, match="LangSmith API key is required"):
            LangChainService(openrouter_api_key="test", langsmith_api_key="")
    
    def test_service_initialization_custom_model(self):
        """Test service initialization with custom model."""
        service = LangChainService(
            openrouter_api_key="test-key",
            langsmith_api_key="langsmith-key",
            default_model="openai/gpt-3.5-turbo"
        )
        
        assert service.default_model == "openai/gpt-3.5-turbo"


class TestContentGenerationRequest:
    """Test cases for ContentGenerationRequest model."""
    
    def test_valid_content_generation_request(self, sample_client_profile):
        """Test creating a valid content generation request."""
        request = ContentGenerationRequest(
            client_profile=sample_client_profile,
            content_type="linkedin_post",
            prompt="Create a LinkedIn post about content strategy",
            context={"topic": "content marketing"}
        )
        
        assert request.content_type == "linkedin_post"
        assert request.prompt == "Create a LinkedIn post about content strategy"
        assert request.context["topic"] == "content marketing"
        assert request.client_profile.name == "Test Client"
    
    def test_content_generation_request_validation(self, sample_client_profile):
        """Test validation of content generation request."""
        # Test missing required fields
        with pytest.raises(ValueError):
            ContentGenerationRequest(
                client_profile=sample_client_profile,
                content_type="",  # Empty content type
                prompt="Test prompt"
            )
        
        with pytest.raises(ValueError):
            ContentGenerationRequest(
                client_profile=sample_client_profile,
                content_type="linkedin_post",
                prompt=""  # Empty prompt
            )


class TestContentGenerationResponse:
    """Test cases for ContentGenerationResponse model."""
    
    def test_valid_content_generation_response(self):
        """Test creating a valid content generation response."""
        response = ContentGenerationResponse(
            content="This is generated content about content strategy.",
            metadata={
                "model": "openai/gpt-4",
                "tokens_used": 150,
                "cost": 0.003
            },
            quality_score=8.5,
            processing_time=2.3
        )
        
        assert response.content == "This is generated content about content strategy."
        assert response.metadata["model"] == "openai/gpt-4"
        assert response.quality_score == 8.5
        assert response.processing_time == 2.3
    
    def test_content_generation_response_validation(self):
        """Test validation of content generation response."""
        # Test quality score range
        with pytest.raises(ValueError):
            ContentGenerationResponse(
                content="Test content",
                quality_score=11.0  # Invalid score > 10
            )
        
        with pytest.raises(ValueError):
            ContentGenerationResponse(
                content="Test content",
                quality_score=-1.0  # Invalid score < 0
            )


class TestBasicContentGeneration:
    """Test cases for basic content generation functionality."""
    
    @pytest.mark.asyncio
    async def test_generate_content_success(self, langchain_service, sample_client_profile):
        """Test successful content generation."""
        with patch.object(langchain_service, '_call_openrouter') as mock_call:
            # Mock the OpenRouter API response
            mock_call.return_value = {
                "choices": [{
                    "message": {
                        "content": "This is a great LinkedIn post about content strategy for SaaS companies."
                    }
                }],
                "usage": {
                    "total_tokens": 120
                }
            }
            
            request = ContentGenerationRequest(
                client_profile=sample_client_profile,
                content_type="linkedin_post",
                prompt="Create a LinkedIn post about content strategy"
            )
            
            response = await langchain_service.generate_content(request)
            
            assert isinstance(response, ContentGenerationResponse)
            assert "content strategy" in response.content.lower()
            assert response.metadata["tokens_used"] == 120
            assert response.quality_score > 0
            
            # Verify the API was called with correct parameters
            mock_call.assert_called_once()
            call_args = mock_call.call_args[0]
            assert "content strategy" in call_args[0].lower()
    
    @pytest.mark.asyncio
    async def test_generate_content_with_context(self, langchain_service, sample_client_profile):
        """Test content generation with additional context."""
        with patch.object(langchain_service, '_call_openrouter') as mock_call:
            mock_call.return_value = {
                "choices": [{
                    "message": {
                        "content": "LinkedIn post about AI in content marketing for SaaS."
                    }
                }],
                "usage": {"total_tokens": 100}
            }
            
            request = ContentGenerationRequest(
                client_profile=sample_client_profile,
                content_type="linkedin_post",
                prompt="Create a LinkedIn post",
                context={
                    "topic": "AI in content marketing",
                    "tone": "professional",
                    "length": "short"
                }
            )
            
            response = await langchain_service.generate_content(request)
            
            assert "AI" in response.content or "ai" in response.content.lower()
            assert response.metadata["tokens_used"] == 100
    
    @pytest.mark.asyncio
    async def test_generate_content_openrouter_error(self, langchain_service, sample_client_profile):
        """Test content generation with OpenRouter API error."""
        with patch.object(langchain_service, '_call_openrouter') as mock_call:
            mock_call.side_effect = OpenRouterError("API rate limit exceeded")
            
            request = ContentGenerationRequest(
                client_profile=sample_client_profile,
                content_type="linkedin_post",
                prompt="Create a LinkedIn post"
            )
            
            with pytest.raises(LangChainError, match="OpenRouter API error"):
                await langchain_service.generate_content(request)
    
    @pytest.mark.asyncio
    async def test_generate_content_invalid_response(self, langchain_service, sample_client_profile):
        """Test content generation with invalid API response."""
        with patch.object(langchain_service, '_call_openrouter') as mock_call:
            # Mock invalid response format
            mock_call.return_value = {
                "choices": [],  # Empty choices
                "usage": {"total_tokens": 0}
            }
            
            request = ContentGenerationRequest(
                client_profile=sample_client_profile,
                content_type="linkedin_post",
                prompt="Create a LinkedIn post"
            )
            
            with pytest.raises(LangChainError, match="Invalid response format"):
                await langchain_service.generate_content(request)


class TestPromptEngineering:
    """Test cases for prompt engineering and client context integration."""
    
    def test_build_system_prompt(self, langchain_service, sample_client_profile):
        """Test building system prompt with client context."""
        system_prompt = langchain_service._build_system_prompt(sample_client_profile)
        
        # Verify client information is included
        assert "SaaS" in system_prompt  # Industry
        assert "thought leadership" in system_prompt.lower()  # Positioning
        assert "educational" in system_prompt.lower()  # Content type preference
        assert "linkedin" in system_prompt.lower()  # Platform
    
    def test_build_user_prompt(self, langchain_service):
        """Test building user prompt with context."""
        context = {
            "topic": "content marketing",
            "tone": "professional",
            "length": "medium"
        }
        
        user_prompt = langchain_service._build_user_prompt(
            "Create a LinkedIn post about content strategy",
            context
        )
        
        assert "content strategy" in user_prompt
        assert "content marketing" in user_prompt
        assert "professional" in user_prompt
        assert "medium" in user_prompt
    
    def test_build_user_prompt_no_context(self, langchain_service):
        """Test building user prompt without additional context."""
        user_prompt = langchain_service._build_user_prompt(
            "Create a LinkedIn post about content strategy",
            None
        )
        
        assert user_prompt == "Create a LinkedIn post about content strategy"


class TestQualityScoring:
    """Test cases for content quality scoring."""
    
    def test_calculate_quality_score(self, langchain_service, sample_client_profile):
        """Test quality score calculation."""
        content = "This is a well-structured LinkedIn post about content strategy for SaaS companies. It provides actionable insights and maintains a professional tone throughout."
        
        score = langchain_service._calculate_quality_score(content, sample_client_profile)
        
        assert 0 <= score <= 10
        assert isinstance(score, float)
    
    def test_calculate_quality_score_short_content(self, langchain_service, sample_client_profile):
        """Test quality score for very short content."""
        content = "Short post."
        
        score = langchain_service._calculate_quality_score(content, sample_client_profile)
        
        # Short content should get lower score
        assert score < 5.0
    
    def test_calculate_quality_score_relevant_content(self, langchain_service, sample_client_profile):
        """Test quality score for content with relevant keywords."""
        content = "Comprehensive guide to SaaS content strategy for building thought leadership in the educational technology space."
        
        score = langchain_service._calculate_quality_score(content, sample_client_profile)
        
        # Content with relevant keywords should get higher score
        assert score >= 6.0


class TestErrorHandling:
    """Test cases for error handling in LangChain service."""
    
    @pytest.mark.asyncio
    async def test_openrouter_connection_error(self, langchain_service, sample_client_profile):
        """Test handling of OpenRouter connection errors."""
        with patch.object(langchain_service, '_call_openrouter') as mock_call:
            mock_call.side_effect = ConnectionError("Failed to connect to OpenRouter")
            
            request = ContentGenerationRequest(
                client_profile=sample_client_profile,
                content_type="linkedin_post",
                prompt="Create a LinkedIn post"
            )
            
            with pytest.raises(LangChainError, match="Connection error"):
                await langchain_service.generate_content(request)
    
    @pytest.mark.asyncio
    async def test_openrouter_timeout_error(self, langchain_service, sample_client_profile):
        """Test handling of OpenRouter timeout errors."""
        with patch.object(langchain_service, '_call_openrouter') as mock_call:
            mock_call.side_effect = TimeoutError("Request timed out")
            
            request = ContentGenerationRequest(
                client_profile=sample_client_profile,
                content_type="linkedin_post",
                prompt="Create a LinkedIn post"
            )
            
            with pytest.raises(LangChainError, match="Request timed out"):
                await langchain_service.generate_content(request)


# Integration test
class TestLangChainServiceIntegration:
    """Integration tests for LangChain service."""
    
    @pytest.mark.asyncio
    async def test_end_to_end_content_generation(self, langchain_service, sample_client_profile):
        """Test end-to-end content generation flow."""
        with patch.object(langchain_service, '_call_openrouter') as mock_call:
            mock_call.return_value = {
                "choices": [{
                    "message": {
                        "content": "🚀 SaaS companies: Your content strategy is your competitive advantage!\n\nIn today's crowded market, thought leadership isn't just nice to have—it's essential. Here's why:\n\n✅ Builds trust before prospects even talk to sales\n✅ Positions your team as industry experts\n✅ Creates organic demand for your solution\n\nThe key? Consistency and authenticity. Share your real insights, not just product features.\n\nWhat's your biggest content challenge? Let's discuss in the comments! 👇\n\n#SaaS #ContentStrategy #ThoughtLeadership"
                    }
                }],
                "usage": {"total_tokens": 180}
            }
            
            request = ContentGenerationRequest(
                client_profile=sample_client_profile,
                content_type="linkedin_post",
                prompt="Create an engaging LinkedIn post about the importance of content strategy for SaaS companies",
                context={
                    "include_emojis": True,
                    "include_hashtags": True,
                    "call_to_action": "engagement"
                }
            )
            
            response = await langchain_service.generate_content(request)
            
            # Verify response structure
            assert isinstance(response, ContentGenerationResponse)
            assert len(response.content) > 0
            assert response.metadata["tokens_used"] == 180
            assert 0 <= response.quality_score <= 10
            assert response.processing_time > 0
            
            # Verify content quality
            content = response.content.lower()
            assert "saas" in content
            assert "content strategy" in content or "content" in content
            assert "#" in response.content  # Has hashtags
            
            # Verify LangSmith tracing was called (if implemented)
            # This would be tested in a real integration scenario
