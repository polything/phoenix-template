"""
Test cases for client data models.
Following TDD methodology - these tests define the expected behavior.
"""

import pytest
from pydantic import ValidationError
from datetime import datetime
from typing import Dict, Any

from backend.models.client import (
    ClientIntakeRequest,
    ClientProfile,
    ServiceOffering,
    ICPProfile,
    ContentPreferences,
    ClientConstraints,
    VoiceExample,
    ProofAsset
)


class TestServiceOffering:
    """Test cases for ServiceOffering model."""
    
    def test_valid_service_offering(self):
        """Test creating a valid service offering."""
        data = {
            "services": ["Content Strategy", "LinkedIn Management"],
            "pricing_tier": "premium",
            "delivery_method": "monthly"
        }
        offering = ServiceOffering(**data)
        assert offering.services == ["Content Strategy", "LinkedIn Management"]
        assert offering.pricing_tier == "premium"
        assert offering.delivery_method == "monthly"
    
    def test_service_offering_requires_services(self):
        """Test that services field is required."""
        with pytest.raises(ValidationError) as exc_info:
            ServiceOffering(pricing_tier="premium")
        
        errors = exc_info.value.errors()
        assert any(error["type"] == "missing" and "services" in str(error) for error in errors)
    
    def test_service_offering_validates_pricing_tier(self):
        """Test that pricing tier is validated."""
        with pytest.raises(ValidationError):
            ServiceOffering(
                services=["Content Strategy"],
                pricing_tier="invalid_tier"
            )


class TestICPProfile:
    """Test cases for ICP (Ideal Customer Profile) model."""
    
    def test_valid_icp_profile(self):
        """Test creating a valid ICP profile."""
        data = {
            "industry": "SaaS",
            "company_size": "10-50 employees",
            "pain_points": ["Inconsistent content", "Low engagement"],
            "budget_range": "£2000-5000/month",
            "decision_makers": ["Marketing Manager", "CEO"]
        }
        icp = ICPProfile(**data)
        assert icp.industry == "SaaS"
        assert len(icp.pain_points) == 2
        assert "Marketing Manager" in icp.decision_makers
    
    def test_icp_profile_requires_core_fields(self):
        """Test that core ICP fields are required."""
        with pytest.raises(ValidationError) as exc_info:
            ICPProfile()
        
        errors = exc_info.value.errors()
        required_fields = {"industry", "company_size", "pain_points"}
        # In Pydantic V2, errors have different structure
        error_messages = [str(error) for error in errors]
        assert all(field in " ".join(error_messages) for field in required_fields)


class TestContentPreferences:
    """Test cases for ContentPreferences model."""
    
    def test_valid_content_preferences(self):
        """Test creating valid content preferences."""
        data = {
            "platforms": ["linkedin", "newsletter"],
            "frequency": "3x per week",
            "content_types": ["educational", "thought_leadership"],
            "tone": "professional but approachable"
        }
        prefs = ContentPreferences(**data)
        assert "linkedin" in prefs.platforms
        assert prefs.tone == "professional but approachable"
    
    def test_content_preferences_validates_platforms(self):
        """Test that platforms are validated against allowed values."""
        valid_platforms = ["linkedin", "newsletter", "blog", "twitter"]
        
        # Valid platforms should work
        prefs = ContentPreferences(
            platforms=["linkedin", "newsletter"],
            frequency="weekly",
            content_types=["educational"]
        )
        assert len(prefs.platforms) == 2
        
        # Invalid platform should fail
        with pytest.raises(ValidationError):
            ContentPreferences(
                platforms=["invalid_platform"],
                frequency="weekly",
                content_types=["educational"]
            )


class TestClientConstraints:
    """Test cases for ClientConstraints model."""
    
    def test_valid_client_constraints(self):
        """Test creating valid client constraints."""
        data = {
            "banned_topics": ["politics", "controversial subjects"],
            "compliance_requirements": ["GDPR", "CCPA"],
            "brand_safety_level": "high",
            "content_approval_required": True
        }
        constraints = ClientConstraints(**data)
        assert "politics" in constraints.banned_topics
        assert constraints.brand_safety_level == "high"
        assert constraints.content_approval_required is True
    
    def test_constraints_validates_brand_safety_level(self):
        """Test that brand safety level is validated."""
        valid_levels = ["low", "medium", "high"]
        
        for level in valid_levels:
            constraints = ClientConstraints(brand_safety_level=level)
            assert constraints.brand_safety_level == level
        
        with pytest.raises(ValidationError):
            ClientConstraints(brand_safety_level="invalid_level")


class TestVoiceExample:
    """Test cases for VoiceExample model."""
    
    def test_valid_voice_example(self):
        """Test creating a valid voice example."""
        data = {
            "content": "This is an example of the client's voice and tone.",
            "platform": "linkedin",
            "content_type": "post",
            "performance_notes": "High engagement, authentic tone"
        }
        voice = VoiceExample(**data)
        assert voice.platform == "linkedin"
        assert "authentic tone" in voice.performance_notes
    
    def test_voice_example_requires_content(self):
        """Test that content field is required."""
        with pytest.raises(ValidationError):
            VoiceExample(platform="linkedin")


class TestProofAsset:
    """Test cases for ProofAsset model."""
    
    def test_valid_proof_asset(self):
        """Test creating a valid proof asset."""
        data = {
            "asset_type": "testimonial",
            "title": "Client Success Story",
            "content": "Amazing results achieved...",
            "source": "John Smith, CEO of TechCorp"
        }
        asset = ProofAsset(**data)
        assert asset.asset_type == "testimonial"
        assert asset.source == "John Smith, CEO of TechCorp"


class TestClientIntakeRequest:
    """Test cases for ClientIntakeRequest model."""
    
    def test_valid_client_intake_request(self):
        """Test creating a valid client intake request."""
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "company": "TechCorp",
            "website": "https://techcorp.com",
            "service_offering": {
                "services": ["Content Strategy"],
                "pricing_tier": "premium"
            },
            "icp_profile": {
                "industry": "SaaS",
                "company_size": "10-50 employees",
                "pain_points": ["Low engagement"]
            },
            "positioning_statement": "We help SaaS companies build thought leadership.",
            "content_preferences": {
                "platforms": ["linkedin"],
                "frequency": "weekly",
                "content_types": ["educational"]
            },
            "constraints": {
                "brand_safety_level": "high"
            }
        }
        
        request = ClientIntakeRequest(**data)
        assert request.name == "John Doe"
        assert request.email == "john@example.com"
        assert request.service_offering.pricing_tier == "premium"
        assert request.icp_profile.industry == "SaaS"
    
    def test_client_intake_validates_email(self):
        """Test that email validation works."""
        base_data = {
            "name": "John Doe",
            "service_offering": {"services": ["Content Strategy"]},
            "icp_profile": {
                "industry": "SaaS",
                "company_size": "10-50",
                "pain_points": ["Low engagement"]
            },
            "positioning_statement": "Test positioning",
            "content_preferences": {
                "platforms": ["linkedin"],
                "frequency": "weekly",
                "content_types": ["educational"]
            }
        }
        
        # Valid email should work
        valid_data = {**base_data, "email": "john@example.com"}
        request = ClientIntakeRequest(**valid_data)
        assert request.email == "john@example.com"
        
        # Invalid email should fail
        with pytest.raises(ValidationError):
            invalid_data = {**base_data, "email": "invalid-email"}
            ClientIntakeRequest(**invalid_data)
    
    def test_client_intake_validates_website_url(self):
        """Test that website URL validation works."""
        base_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "service_offering": {"services": ["Content Strategy"]},
            "icp_profile": {
                "industry": "SaaS",
                "company_size": "10-50",
                "pain_points": ["Low engagement"]
            },
            "positioning_statement": "Test positioning",
            "content_preferences": {
                "platforms": ["linkedin"],
                "frequency": "weekly",
                "content_types": ["educational"]
            }
        }
        
        # Valid URLs should work
        valid_urls = [
            "https://example.com",
            "http://example.com",
            "https://subdomain.example.com/path"
        ]
        
        for url in valid_urls:
            data = {**base_data, "website": url}
            request = ClientIntakeRequest(**data)
            assert str(request.website) == url or str(request.website) == url + "/"
        
        # Invalid URL should fail
        with pytest.raises(ValidationError):
            invalid_data = {**base_data, "website": "not-a-url"}
            ClientIntakeRequest(**invalid_data)
    
    def test_client_intake_requires_core_fields(self):
        """Test that core fields are required."""
        with pytest.raises(ValidationError) as exc_info:
            ClientIntakeRequest()
        
        errors = exc_info.value.errors()
        required_fields = {
            "name", "email", "service_offering", "icp_profile", 
            "positioning_statement", "content_preferences"
        }
        # In Pydantic V2, errors have different structure
        error_messages = [str(error) for error in errors]
        assert all(field in " ".join(error_messages) for field in required_fields)


class TestClientProfile:
    """Test cases for ClientProfile model (database representation)."""
    
    def test_valid_client_profile(self):
        """Test creating a valid client profile."""
        data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "John Doe",
            "email": "john@example.com",
            "service_offering": {"services": ["Content Strategy"]},
            "icp_profile": {
                "industry": "SaaS",
                "company_size": "10-50",
                "pain_points": ["Low engagement"]
            },
            "positioning_statement": "Test positioning",
            "content_preferences": {
                "platforms": ["linkedin"],
                "frequency": "weekly",
                "content_types": ["educational"]
            },
            "status": "active",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        profile = ClientProfile(**data)
        assert profile.name == "John Doe"
        assert profile.status == "active"
        assert isinstance(profile.created_at, datetime)
    
    def test_client_profile_default_status(self):
        """Test that client profile has default status."""
        minimal_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "service_offering": {"services": ["Content Strategy"]},
            "icp_profile": {
                "industry": "SaaS",
                "company_size": "10-50",
                "pain_points": ["Low engagement"]
            },
            "positioning_statement": "Test positioning",
            "content_preferences": {
                "platforms": ["linkedin"],
                "frequency": "weekly",
                "content_types": ["educational"]
            }
        }
        
        profile = ClientProfile(**minimal_data)
        assert profile.status == "active"  # Default value
    
    def test_client_profile_validates_status(self):
        """Test that status field is validated."""
        base_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "service_offering": {"services": ["Content Strategy"]},
            "icp_profile": {
                "industry": "SaaS",
                "company_size": "10-50",
                "pain_points": ["Low engagement"]
            },
            "positioning_statement": "Test positioning",
            "content_preferences": {
                "platforms": ["linkedin"],
                "frequency": "weekly",
                "content_types": ["educational"]
            }
        }
        
        # Valid statuses should work
        valid_statuses = ["active", "inactive", "pending"]
        for status in valid_statuses:
            data = {**base_data, "status": status}
            profile = ClientProfile(**data)
            assert profile.status == status
        
        # Invalid status should fail
        with pytest.raises(ValidationError):
            invalid_data = {**base_data, "status": "invalid_status"}
            ClientProfile(**invalid_data)


# Integration test to ensure all models work together
class TestModelIntegration:
    """Integration tests for model relationships."""
    
    def test_client_intake_to_profile_conversion(self):
        """Test converting intake request to client profile."""
        intake_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "company": "TechCorp",
            "website": "https://techcorp.com",
            "service_offering": {
                "services": ["Content Strategy", "LinkedIn Management"],
                "pricing_tier": "premium"
            },
            "icp_profile": {
                "industry": "SaaS",
                "company_size": "10-50 employees",
                "pain_points": ["Inconsistent content", "Low engagement"],
                "budget_range": "£2000-5000/month"
            },
            "positioning_statement": "We help SaaS companies build thought leadership through strategic content.",
            "content_preferences": {
                "platforms": ["linkedin", "newsletter"],
                "frequency": "3x per week",
                "content_types": ["educational", "thought_leadership"],
                "tone": "professional but approachable"
            },
            "constraints": {
                "banned_topics": ["politics"],
                "brand_safety_level": "high",
                "content_approval_required": True
            },
            "voice_examples": [
                {
                    "content": "Example voice content",
                    "platform": "linkedin",
                    "content_type": "post"
                }
            ],
            "proof_assets": [
                {
                    "asset_type": "testimonial",
                    "title": "Client Success",
                    "content": "Great results achieved"
                }
            ]
        }
        
        # Create intake request
        intake_request = ClientIntakeRequest(**intake_data)
        assert intake_request.name == "John Doe"
        
        # Convert to client profile (simulate what the API would do)
        profile_data = {
            **intake_request.model_dump(),
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        client_profile = ClientProfile(**profile_data)
        assert client_profile.name == intake_request.name
        assert client_profile.email == intake_request.email
        assert client_profile.service_offering.pricing_tier == "premium"
