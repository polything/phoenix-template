"""
Client data models for the AI-Enhanced Autonomous Content Pipeline.
Defines Pydantic models for client intake, profiles, and related data structures.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from enum import Enum

from pydantic import BaseModel, EmailStr, HttpUrl, Field, field_validator, ConfigDict


class PricingTier(str, Enum):
    """Enum for pricing tiers."""
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class BrandSafetyLevel(str, Enum):
    """Enum for brand safety levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ClientStatus(str, Enum):
    """Enum for client status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


class Platform(str, Enum):
    """Enum for supported platforms."""
    LINKEDIN = "linkedin"
    NEWSLETTER = "newsletter"
    BLOG = "blog"
    TWITTER = "twitter"


class ContentType(str, Enum):
    """Enum for content types."""
    EDUCATIONAL = "educational"
    THOUGHT_LEADERSHIP = "thought_leadership"
    PROMOTIONAL = "promotional"
    CASE_STUDY = "case_study"
    NEWS = "news"


class AssetType(str, Enum):
    """Enum for proof asset types."""
    TESTIMONIAL = "testimonial"
    CASE_STUDY = "case_study"
    CREDENTIAL = "credential"
    AWARD = "award"
    CERTIFICATION = "certification"
    MEDIA_MENTION = "media_mention"


class ServiceOffering(BaseModel):
    """Model for client service offering details."""
    
    services: List[str] = Field(
        ..., 
        min_length=1,
        description="List of services offered by the client"
    )
    pricing_tier: Optional[PricingTier] = Field(
        None,
        description="Pricing tier (basic, standard, premium, enterprise)"
    )
    delivery_method: Optional[str] = Field(
        None,
        description="How services are delivered (e.g., monthly, project-based)"
    )
    target_market: Optional[str] = Field(
        None,
        description="Primary target market or industry focus"
    )
    
    model_config = ConfigDict(use_enum_values=True)


class ICPProfile(BaseModel):
    """Model for Ideal Customer Profile."""
    
    industry: str = Field(
        ...,
        description="Primary industry of ideal customers"
    )
    company_size: str = Field(
        ...,
        description="Size range of target companies (e.g., '10-50 employees')"
    )
    pain_points: List[str] = Field(
        ...,
        min_length=1,
        description="Key pain points that the client solves"
    )
    budget_range: Optional[str] = Field(
        None,
        description="Typical budget range of ideal customers"
    )
    decision_makers: Optional[List[str]] = Field(
        default_factory=list,
        description="Typical decision maker roles"
    )
    geographic_focus: Optional[str] = Field(
        None,
        description="Geographic market focus"
    )
    company_stage: Optional[str] = Field(
        None,
        description="Stage of companies (startup, growth, mature)"
    )


class ContentPreferences(BaseModel):
    """Model for client content preferences."""
    
    platforms: List[Platform] = Field(
        ...,
        min_length=1,
        description="Preferred content platforms"
    )
    frequency: str = Field(
        ...,
        description="Desired content frequency (e.g., '3x per week')"
    )
    content_types: List[ContentType] = Field(
        ...,
        min_length=1,
        description="Preferred content types"
    )
    tone: Optional[str] = Field(
        None,
        description="Preferred tone and style"
    )
    topics_of_interest: Optional[List[str]] = Field(
        default_factory=list,
        description="Specific topics the client wants to cover"
    )
    content_length_preference: Optional[str] = Field(
        None,
        description="Preferred content length (short, medium, long)"
    )
    
    model_config = ConfigDict(use_enum_values=True)


class ClientConstraints(BaseModel):
    """Model for client constraints and compliance requirements."""
    
    banned_topics: Optional[List[str]] = Field(
        default_factory=list,
        description="Topics to avoid in content"
    )
    compliance_requirements: Optional[List[str]] = Field(
        default_factory=list,
        description="Regulatory compliance requirements (GDPR, CCPA, etc.)"
    )
    brand_safety_level: BrandSafetyLevel = Field(
        default=BrandSafetyLevel.MEDIUM,
        description="Brand safety level (low, medium, high)"
    )
    content_approval_required: bool = Field(
        default=True,
        description="Whether content requires approval before publishing"
    )
    competitor_mentions: Optional[str] = Field(
        None,
        description="Policy on mentioning competitors"
    )
    sensitive_topics: Optional[List[str]] = Field(
        default_factory=list,
        description="Topics that require special handling"
    )
    
    model_config = ConfigDict(use_enum_values=True)


class VoiceExample(BaseModel):
    """Model for client voice and tone examples."""
    
    content: str = Field(
        ...,
        min_length=10,
        description="Example content that represents the client's voice"
    )
    platform: Platform = Field(
        ...,
        description="Platform where this example was published"
    )
    content_type: Optional[str] = Field(
        None,
        description="Type of content (post, article, comment, etc.)"
    )
    performance_notes: Optional[str] = Field(
        None,
        description="Notes about how this content performed"
    )
    date_published: Optional[datetime] = Field(
        None,
        description="When this content was originally published"
    )
    
    model_config = ConfigDict(use_enum_values=True)


class ProofAsset(BaseModel):
    """Model for client proof assets (testimonials, case studies, etc.)."""
    
    asset_type: AssetType = Field(
        ...,
        description="Type of proof asset"
    )
    title: str = Field(
        ...,
        min_length=1,
        description="Title or headline of the asset"
    )
    content: Optional[str] = Field(
        None,
        description="Full content of the asset"
    )
    source: Optional[str] = Field(
        None,
        description="Source or attribution (person, company, publication)"
    )
    url: Optional[HttpUrl] = Field(
        None,
        description="URL to the original asset if available"
    )
    date: Optional[datetime] = Field(
        None,
        description="Date of the asset"
    )
    metrics: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Performance metrics or results achieved"
    )
    
    model_config = ConfigDict(use_enum_values=True)


class ClientIntakeRequest(BaseModel):
    """Model for client intake form submission."""
    
    # Basic Information
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Client's full name"
    )
    email: EmailStr = Field(
        ...,
        description="Client's email address"
    )
    company: Optional[str] = Field(
        None,
        max_length=255,
        description="Company name"
    )
    website: Optional[HttpUrl] = Field(
        None,
        description="Company website URL"
    )
    
    # Core Business Information
    service_offering: ServiceOffering = Field(
        ...,
        description="Details about what the client offers"
    )
    icp_profile: ICPProfile = Field(
        ...,
        description="Ideal Customer Profile details"
    )
    positioning_statement: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="Client's unique positioning statement"
    )
    
    # Content Strategy
    content_preferences: ContentPreferences = Field(
        ...,
        description="Content preferences and requirements"
    )
    constraints: Optional[ClientConstraints] = Field(
        default_factory=ClientConstraints,
        description="Content constraints and compliance requirements"
    )
    
    # Supporting Materials
    voice_examples: Optional[List[VoiceExample]] = Field(
        default_factory=list,
        description="Examples of the client's voice and tone"
    )
    proof_assets: Optional[List[ProofAsset]] = Field(
        default_factory=list,
        description="Testimonials, case studies, and other proof assets"
    )
    
    # Additional Information
    additional_notes: Optional[str] = Field(
        None,
        max_length=2000,
        description="Any additional notes or requirements"
    )
    
    @field_validator('voice_examples')
    @classmethod
    def validate_voice_examples(cls, v):
        """Validate voice examples list."""
        if v and len(v) > 10:
            raise ValueError('Maximum 10 voice examples allowed')
        return v
    
    @field_validator('proof_assets')
    @classmethod
    def validate_proof_assets(cls, v):
        """Validate proof assets list."""
        if v and len(v) > 20:
            raise ValueError('Maximum 20 proof assets allowed')
        return v


class ClientProfile(BaseModel):
    """Model for stored client profile (database representation)."""
    
    # Database fields
    id: Optional[UUID] = Field(
        default_factory=uuid4,
        description="Unique client identifier"
    )
    
    # Inherit all fields from intake request
    name: str
    email: EmailStr
    company: Optional[str] = None
    website: Optional[HttpUrl] = None
    
    service_offering: ServiceOffering
    icp_profile: ICPProfile
    positioning_statement: str
    content_preferences: ContentPreferences
    constraints: Optional[ClientConstraints] = Field(default_factory=ClientConstraints)
    
    voice_examples: Optional[List[VoiceExample]] = Field(default_factory=list)
    proof_assets: Optional[List[ProofAsset]] = Field(default_factory=list)
    additional_notes: Optional[str] = None
    
    # Database metadata
    status: ClientStatus = Field(
        default=ClientStatus.ACTIVE,
        description="Client status"
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="When the client was created"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="When the client was last updated"
    )
    
    # Vector embeddings (for semantic search)
    voice_embedding: Optional[List[float]] = Field(
        None,
        description="Vector embedding of client's voice/style"
    )
    
    model_config = ConfigDict(
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
            UUID: str
        }
    )
    
    @classmethod
    def from_intake_request(cls, intake_request: ClientIntakeRequest) -> "ClientProfile":
        """Create a ClientProfile from a ClientIntakeRequest."""
        return cls(**intake_request.model_dump())


class ClientProfileUpdate(BaseModel):
    """Model for updating client profiles (partial updates allowed)."""
    
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    company: Optional[str] = None
    website: Optional[HttpUrl] = None
    
    service_offering: Optional[ServiceOffering] = None
    icp_profile: Optional[ICPProfile] = None
    positioning_statement: Optional[str] = None
    content_preferences: Optional[ContentPreferences] = None
    constraints: Optional[ClientConstraints] = None
    
    voice_examples: Optional[List[VoiceExample]] = None
    proof_assets: Optional[List[ProofAsset]] = None
    additional_notes: Optional[str] = None
    
    status: Optional[ClientStatus] = None
    
    model_config = ConfigDict(use_enum_values=True)


# Response models for API
class ClientProfileResponse(BaseModel):
    """Response model for client profile API endpoints."""
    
    id: UUID
    name: str
    email: EmailStr
    company: Optional[str]
    website: Optional[HttpUrl]
    status: ClientStatus
    created_at: datetime
    updated_at: datetime
    
    # Include summary information
    service_summary: str = Field(
        ...,
        description="Summary of client's services"
    )
    platform_count: int = Field(
        ...,
        description="Number of platforms client uses"
    )
    
    model_config = ConfigDict(
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
            UUID: str
        }
    )
    
    @classmethod
    def from_client_profile(cls, profile: ClientProfile) -> "ClientProfileResponse":
        """Create response from client profile."""
        return cls(
            id=profile.id,
            name=profile.name,
            email=profile.email,
            company=profile.company,
            website=profile.website,
            status=profile.status,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
            service_summary=", ".join(profile.service_offering.services),
            platform_count=len(profile.content_preferences.platforms)
        )


class ClientListResponse(BaseModel):
    """Response model for client list API endpoint."""
    
    clients: List[ClientProfileResponse]
    total: int
    page: int
    page_size: int
    
    model_config = ConfigDict(use_enum_values=True)
