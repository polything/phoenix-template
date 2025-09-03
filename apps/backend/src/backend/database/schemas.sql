-- AI-Enhanced Autonomous Content Pipeline Database Schema
-- Project Phoenix - Supabase PostgreSQL Schema

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgvector";

-- ==============================================================================
-- CLIENTS TABLE
-- Stores comprehensive client intake data and profile information
-- ==============================================================================

CREATE TABLE clients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Basic Client Information
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    company VARCHAR(255),
    website VARCHAR(500),
    
    -- Service Offering & Positioning
    service_offering JSONB NOT NULL, -- What they sell/offer
    icp_profile JSONB NOT NULL, -- Ideal Customer Profile details
    positioning_statement TEXT NOT NULL, -- Their unique positioning
    
    -- Voice & Brand Guidelines
    voice_examples JSONB, -- Sample content that represents their voice
    brand_guidelines JSONB, -- Colors, fonts, style preferences
    
    -- Proof Assets & Social Proof
    proof_assets JSONB, -- Testimonials, case studies, credentials
    
    -- Content Preferences & Constraints
    content_preferences JSONB NOT NULL, -- Platform preferences, frequency, topics
    constraints JSONB, -- Banned topics, compliance requirements
    
    -- Metadata
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'pending')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Vector embeddings for semantic search (client voice/style)
    voice_embedding vector(1536), -- OpenAI embedding dimension
    
    -- Indexes
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- ==============================================================================
-- CONTENT_PIPELINE_RUNS TABLE
-- Tracks each execution of the content pipeline for a client
-- ==============================================================================

CREATE TABLE content_pipeline_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    
    -- Pipeline Execution Details
    status VARCHAR(50) DEFAULT 'pending' CHECK (
        status IN ('pending', 'running', 'completed', 'failed', 'cancelled')
    ),
    stage VARCHAR(100) NOT NULL, -- Current or completed stage
    
    -- Input Data
    input_data JSONB NOT NULL, -- Original request/brief
    
    -- Stage Outputs (structured JSON for each pipeline stage)
    research_output JSONB, -- Market research results
    opportunity_mapping JSONB, -- Opportunity clusters and priority scores
    angle_matrix JSONB, -- Content angles mapped to pain points
    content_outline JSONB, -- Structured content outline
    draft_content JSONB, -- Generated content draft
    final_content JSONB, -- Reviewed and approved content
    
    -- Quality & Compliance
    quality_score DECIMAL(3,1) CHECK (quality_score >= 0 AND quality_score <= 10),
    compliance_checks JSONB, -- Results of compliance validation
    human_review_required BOOLEAN DEFAULT FALSE,
    
    -- Performance Tracking
    processing_time_seconds INTEGER,
    ai_model_calls JSONB, -- Track which models were used and costs
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    
    -- Indexes for performance
    INDEX idx_pipeline_runs_client_id ON content_pipeline_runs(client_id),
    INDEX idx_pipeline_runs_status ON content_pipeline_runs(status),
    INDEX idx_pipeline_runs_created_at ON content_pipeline_runs(created_at DESC)
);

-- ==============================================================================
-- RESEARCH_SOURCES TABLE
-- Stores validated research sources and their credibility scores
-- ==============================================================================

CREATE TABLE research_sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Source Information
    url VARCHAR(2000) NOT NULL UNIQUE,
    domain VARCHAR(500) NOT NULL,
    title VARCHAR(1000),
    source_type VARCHAR(100) CHECK (
        source_type IN ('news', 'blog', 'forum', 'academic', 'industry_report', 'social_media', 'other')
    ),
    
    -- Credibility Assessment
    credibility_score DECIMAL(3,1) CHECK (credibility_score >= 0 AND credibility_score <= 10),
    credibility_factors JSONB, -- Factors that influenced the score
    
    -- Content Analysis
    content_summary TEXT,
    key_insights JSONB,
    relevance_tags VARCHAR(255)[],
    
    -- Usage Tracking
    times_referenced INTEGER DEFAULT 0,
    last_used_at TIMESTAMP WITH TIME ZONE,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Indexes
    INDEX idx_research_sources_domain ON research_sources(domain),
    INDEX idx_research_sources_credibility ON research_sources(credibility_score DESC),
    INDEX idx_research_sources_last_used ON research_sources(last_used_at DESC)
);

-- ==============================================================================
-- CONTENT_PERFORMANCE TABLE
-- Tracks performance metrics for published content
-- ==============================================================================

CREATE TABLE content_performance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pipeline_run_id UUID NOT NULL REFERENCES content_pipeline_runs(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    
    -- Content Identification
    content_type VARCHAR(100) NOT NULL CHECK (
        content_type IN ('linkedin_post', 'newsletter', 'blog_post', 'lead_magnet', 'other')
    ),
    platform VARCHAR(100) NOT NULL,
    content_url VARCHAR(2000),
    
    -- Performance Metrics
    views INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    engagements INTEGER DEFAULT 0, -- Likes, comments, shares combined
    conversions INTEGER DEFAULT 0, -- Sign-ups, downloads, etc.
    
    -- Calculated Metrics
    ctr DECIMAL(5,4) GENERATED ALWAYS AS (
        CASE WHEN views > 0 THEN ROUND((clicks::DECIMAL / views::DECIMAL) * 100, 4) ELSE 0 END
    ) STORED,
    engagement_rate DECIMAL(5,4) GENERATED ALWAYS AS (
        CASE WHEN views > 0 THEN ROUND((engagements::DECIMAL / views::DECIMAL) * 100, 4) ELSE 0 END
    ) STORED,
    conversion_rate DECIMAL(5,4) GENERATED ALWAYS AS (
        CASE WHEN clicks > 0 THEN ROUND((conversions::DECIMAL / clicks::DECIMAL) * 100, 4) ELSE 0 END
    ) STORED,
    
    -- UTM Tracking
    utm_source VARCHAR(255),
    utm_medium VARCHAR(255),
    utm_campaign VARCHAR(255),
    utm_content VARCHAR(255),
    
    -- Time Tracking
    published_at TIMESTAMP WITH TIME ZONE NOT NULL,
    last_updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Indexes
    INDEX idx_content_performance_client_id ON content_performance(client_id),
    INDEX idx_content_performance_pipeline_run ON content_performance(pipeline_run_id),
    INDEX idx_content_performance_published_at ON content_performance(published_at DESC),
    INDEX idx_content_performance_ctr ON content_performance(ctr DESC),
    INDEX idx_content_performance_conversion_rate ON content_performance(conversion_rate DESC)
);

-- ==============================================================================
-- KNOWLEDGE_BASE TABLE
-- Stores learnings, winning patterns, and voice refinements
-- ==============================================================================

CREATE TABLE knowledge_base (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE, -- NULL for global insights
    
    -- Knowledge Classification
    knowledge_type VARCHAR(100) NOT NULL CHECK (
        knowledge_type IN ('winning_hook', 'successful_angle', 'voice_refinement', 
                          'pain_point', 'objection_handling', 'cta_pattern', 'other')
    ),
    category VARCHAR(255),
    
    -- Content
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    context JSONB, -- When/where this was learned
    
    -- Performance Data
    success_score DECIMAL(3,1) CHECK (success_score >= 0 AND success_score <= 10),
    usage_count INTEGER DEFAULT 0,
    last_used_at TIMESTAMP WITH TIME ZONE,
    
    -- Vector Search
    content_embedding vector(1536),
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Indexes
    INDEX idx_knowledge_base_client_id ON knowledge_base(client_id),
    INDEX idx_knowledge_base_type ON knowledge_base(knowledge_type),
    INDEX idx_knowledge_base_success_score ON knowledge_base(success_score DESC)
);

-- ==============================================================================
-- TRIGGERS FOR UPDATED_AT TIMESTAMPS
-- ==============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers to relevant tables
CREATE TRIGGER update_clients_updated_at BEFORE UPDATE ON clients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_research_sources_updated_at BEFORE UPDATE ON research_sources
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_knowledge_base_updated_at BEFORE UPDATE ON knowledge_base
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ==============================================================================
-- INITIAL SEED DATA (Optional - for development/testing)
-- ==============================================================================

-- Example client for testing (will be removed in production)
INSERT INTO clients (
    name, email, company, website,
    service_offering, icp_profile, positioning_statement,
    content_preferences, constraints
) VALUES (
    'Test Marketing Strategist',
    'test@example.com',
    'Phoenix Digital',
    'https://phoenix-digital.example.com',
    '{"services": ["Content Strategy", "LinkedIn Management", "Newsletter Marketing"], "pricing": "Premium", "delivery": "Monthly"}',
    '{"industry": "SaaS", "company_size": "10-50 employees", "pain_points": ["Inconsistent content", "Low engagement"], "budget": "£2000-5000/month"}',
    'We help SaaS companies build authentic thought leadership through strategic content that drives qualified leads.',
    '{"platforms": ["linkedin", "newsletter"], "frequency": "3x per week", "content_types": ["educational", "thought_leadership"], "tone": "professional but approachable"}',
    '{"banned_topics": ["politics", "controversial subjects"], "compliance": ["GDPR"], "brand_safety": "high"}'
);

-- ==============================================================================
-- VIEWS FOR COMMON QUERIES
-- ==============================================================================

-- Active pipeline runs with client information
CREATE VIEW active_pipeline_runs AS
SELECT 
    pr.id,
    pr.client_id,
    c.name AS client_name,
    c.email AS client_email,
    pr.status,
    pr.stage,
    pr.created_at,
    pr.processing_time_seconds,
    pr.quality_score
FROM content_pipeline_runs pr
JOIN clients c ON pr.client_id = c.id
WHERE pr.status IN ('pending', 'running');

-- Performance summary by client
CREATE VIEW client_performance_summary AS
SELECT 
    c.id AS client_id,
    c.name AS client_name,
    COUNT(cp.id) AS total_content_pieces,
    AVG(cp.ctr) AS avg_ctr,
    AVG(cp.engagement_rate) AS avg_engagement_rate,
    AVG(cp.conversion_rate) AS avg_conversion_rate,
    SUM(cp.views) AS total_views,
    SUM(cp.conversions) AS total_conversions
FROM clients c
LEFT JOIN content_performance cp ON c.id = cp.client_id
GROUP BY c.id, c.name;

-- ==============================================================================
-- ROW LEVEL SECURITY (RLS) - Enable when authentication is implemented
-- ==============================================================================

-- Enable RLS on sensitive tables (uncomment when auth is ready)
-- ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE content_pipeline_runs ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE content_performance ENABLE ROW LEVEL SECURITY;

-- Example RLS policy (uncomment and modify when auth is implemented)
-- CREATE POLICY "Users can only see their own clients" ON clients
--     FOR ALL USING (auth.uid() = user_id);

-- ==============================================================================
-- COMMENTS FOR DOCUMENTATION
-- ==============================================================================

COMMENT ON TABLE clients IS 'Stores comprehensive client intake data and profiles for the AI content pipeline';
COMMENT ON TABLE content_pipeline_runs IS 'Tracks each execution of the content generation pipeline with stage outputs';
COMMENT ON TABLE research_sources IS 'Validated research sources with credibility scores for content generation';
COMMENT ON TABLE content_performance IS 'Performance metrics for published content across platforms';
COMMENT ON TABLE knowledge_base IS 'Accumulated learnings, patterns, and refinements for improving content quality';

COMMENT ON COLUMN clients.voice_embedding IS 'Vector embedding of client voice/style for semantic similarity matching';
COMMENT ON COLUMN clients.icp_profile IS 'Ideal Customer Profile - detailed audience characteristics and pain points';
COMMENT ON COLUMN content_pipeline_runs.ai_model_calls IS 'Tracks AI model usage, costs, and performance for each pipeline run';
COMMENT ON COLUMN research_sources.credibility_score IS 'Automated credibility assessment score (0-10) based on domain authority, recency, etc.';
