"""
Test cases for client API endpoints.
Following TDD methodology - these tests define the expected API behavior.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from uuid import uuid4
from datetime import datetime

from backend.main import app
from backend.models.client import (
    ClientIntakeRequest,
    ClientProfile,
    ClientProfileResponse,
    ClientListResponse
)


@pytest.fixture
def client():
    """Create a test client for FastAPI."""
    return TestClient(app)


@pytest.fixture
def sample_intake_data():
    """Sample client intake data for testing."""
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "company": "TechCorp",
        "website": "https://techcorp.com",
        "service_offering": {
            "services": ["Content Strategy", "LinkedIn Management"],
            "pricing_tier": "premium",
            "delivery_method": "monthly"
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
        }
    }


@pytest.fixture
def sample_client_profile():
    """Sample client profile for testing."""
    return ClientProfile(
        id=uuid4(),
        name="John Doe",
        email="john@example.com",
        company="TechCorp",
        service_offering={
            "services": ["Content Strategy"],
            "pricing_tier": "premium"
        },
        icp_profile={
            "industry": "SaaS",
            "company_size": "10-50",
            "pain_points": ["Low engagement"]
        },
        positioning_statement="Test positioning",
        content_preferences={
            "platforms": ["linkedin"],
            "frequency": "weekly",
            "content_types": ["educational"]
        },
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


class TestClientIntakeEndpoint:
    """Test cases for POST /api/clients/intake endpoint."""
    
    def test_create_client_intake_success(self, client, sample_intake_data):
        """Test successful client intake creation."""
        with patch('backend.api.clients.create_client_from_intake') as mock_create:
            # Mock the service function
            mock_profile = ClientProfile(**sample_intake_data)
            mock_create.return_value = mock_profile
            
            response = client.post("/api/clients/intake", json=sample_intake_data)
            
            assert response.status_code == 201
            data = response.json()
            assert data["name"] == "John Doe"
            assert data["email"] == "john@example.com"
            assert data["status"] == "active"
            assert "id" in data
            assert "created_at" in data
            
            # Verify the service was called with correct data
            mock_create.assert_called_once()
            call_args = mock_create.call_args[0][0]
            assert isinstance(call_args, ClientIntakeRequest)
            assert call_args.name == "John Doe"
    
    def test_create_client_intake_validation_error(self, client):
        """Test client intake creation with invalid data."""
        invalid_data = {
            "name": "",  # Empty name should fail validation
            "email": "invalid-email",  # Invalid email format
        }
        
        response = client.post("/api/clients/intake", json=invalid_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        # Should contain validation errors
        assert any("name" in str(error) for error in data["detail"])
        assert any("email" in str(error) for error in data["detail"])
    
    def test_create_client_intake_duplicate_email(self, client, sample_intake_data):
        """Test client intake creation with duplicate email."""
        with patch('backend.api.clients.create_client_from_intake') as mock_create:
            # Mock a duplicate email error
            from backend.api.clients import DuplicateEmailError
            mock_create.side_effect = DuplicateEmailError("Email already exists")
            
            response = client.post("/api/clients/intake", json=sample_intake_data)
            
            assert response.status_code == 409
            data = response.json()
            assert "already exists" in data["detail"].lower()
    
    def test_create_client_intake_server_error(self, client, sample_intake_data):
        """Test client intake creation with server error."""
        with patch('backend.api.clients.create_client_from_intake') as mock_create:
            # Mock a server error
            mock_create.side_effect = Exception("Database connection failed")
            
            response = client.post("/api/clients/intake", json=sample_intake_data)
            
            assert response.status_code == 500
            data = response.json()
            assert "internal server error" in data["detail"].lower()


class TestGetClientsEndpoint:
    """Test cases for GET /api/clients endpoint."""
    
    def test_get_clients_success(self, client):
        """Test successful retrieval of client list."""
        with patch('backend.api.clients.get_clients_list') as mock_get:
            # Mock the service function
            mock_clients = [
                ClientProfileResponse(
                    id=uuid4(),
                    name="John Doe",
                    email="john@example.com",
                    company="TechCorp",
                    website=None,
                    status="active",
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    service_summary="Content Strategy",
                    platform_count=1
                ),
                ClientProfileResponse(
                    id=uuid4(),
                    name="Jane Smith",
                    email="jane@example.com",
                    company="StartupCo",
                    website=None,
                    status="active",
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    service_summary="LinkedIn Management",
                    platform_count=2
                )
            ]
            mock_response = ClientListResponse(
                clients=mock_clients,
                total=2,
                page=1,
                page_size=10
            )
            mock_get.return_value = mock_response
            
            response = client.get("/api/clients")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 2
            assert len(data["clients"]) == 2
            assert data["clients"][0]["name"] == "John Doe"
            assert data["clients"][1]["name"] == "Jane Smith"
    
    def test_get_clients_with_pagination(self, client):
        """Test client list retrieval with pagination parameters."""
        with patch('backend.api.clients.get_clients_list') as mock_get:
            mock_response = ClientListResponse(
                clients=[],
                total=0,
                page=2,
                page_size=5
            )
            mock_get.return_value = mock_response
            
            response = client.get("/api/clients?page=2&page_size=5")
            
            assert response.status_code == 200
            data = response.json()
            assert data["page"] == 2
            assert data["page_size"] == 5
            
            # Verify service was called with correct parameters
            mock_get.assert_called_once_with(page=2, page_size=5, search=None)
    
    def test_get_clients_with_search(self, client):
        """Test client list retrieval with search parameter."""
        with patch('backend.api.clients.get_clients_list') as mock_get:
            mock_response = ClientListResponse(
                clients=[],
                total=0,
                page=1,
                page_size=10
            )
            mock_get.return_value = mock_response
            
            response = client.get("/api/clients?search=TechCorp")
            
            assert response.status_code == 200
            
            # Verify service was called with search parameter
            mock_get.assert_called_once_with(page=1, page_size=10, search="TechCorp")


class TestGetClientByIdEndpoint:
    """Test cases for GET /api/clients/{client_id} endpoint."""
    
    def test_get_client_by_id_success(self, client, sample_client_profile):
        """Test successful retrieval of client by ID."""
        with patch('backend.api.clients.get_client_by_id') as mock_get:
            mock_get.return_value = sample_client_profile
            
            client_id = str(sample_client_profile.id)
            response = client.get(f"/api/clients/{client_id}")
            
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "John Doe"
            assert data["email"] == "john@example.com"
            assert data["id"] == client_id
    
    def test_get_client_by_id_not_found(self, client):
        """Test retrieval of non-existent client."""
        with patch('backend.api.clients.get_client_by_id') as mock_get:
            from backend.api.clients import ClientNotFoundError
            mock_get.side_effect = ClientNotFoundError("Client not found")
            
            fake_id = str(uuid4())
            response = client.get(f"/api/clients/{fake_id}")
            
            assert response.status_code == 404
            data = response.json()
            assert "not found" in data["detail"].lower()
    
    def test_get_client_by_id_invalid_uuid(self, client):
        """Test retrieval with invalid UUID format."""
        response = client.get("/api/clients/invalid-uuid")
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data


class TestUpdateClientEndpoint:
    """Test cases for PUT /api/clients/{client_id} endpoint."""
    
    def test_update_client_success(self, client, sample_client_profile):
        """Test successful client update."""
        with patch('backend.api.clients.update_client') as mock_update:
            updated_profile = sample_client_profile.model_copy()
            updated_profile.name = "John Updated"
            mock_update.return_value = updated_profile
            
            update_data = {
                "name": "John Updated",
                "company": "UpdatedCorp"
            }
            
            client_id = str(sample_client_profile.id)
            response = client.put(f"/api/clients/{client_id}", json=update_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "John Updated"
    
    def test_update_client_not_found(self, client):
        """Test update of non-existent client."""
        with patch('backend.api.clients.update_client') as mock_update:
            from backend.api.clients import ClientNotFoundError
            mock_update.side_effect = ClientNotFoundError("Client not found")
            
            update_data = {"name": "Updated Name"}
            fake_id = str(uuid4())
            response = client.put(f"/api/clients/{fake_id}", json=update_data)
            
            assert response.status_code == 404


class TestDeleteClientEndpoint:
    """Test cases for DELETE /api/clients/{client_id} endpoint."""
    
    def test_delete_client_success(self, client):
        """Test successful client deletion."""
        with patch('backend.api.clients.delete_client') as mock_delete:
            mock_delete.return_value = True
            
            fake_id = str(uuid4())
            response = client.delete(f"/api/clients/{fake_id}")
            
            assert response.status_code == 204
            assert response.content == b""
    
    def test_delete_client_not_found(self, client):
        """Test deletion of non-existent client."""
        with patch('backend.api.clients.delete_client') as mock_delete:
            from backend.api.clients import ClientNotFoundError
            mock_delete.side_effect = ClientNotFoundError("Client not found")
            
            fake_id = str(uuid4())
            response = client.delete(f"/api/clients/{fake_id}")
            
            assert response.status_code == 404


class TestHealthCheckEndpoint:
    """Test cases for health check endpoint."""
    
    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data


# Integration tests that test the full request/response cycle
class TestClientAPIIntegration:
    """Integration tests for client API endpoints."""
    
    def test_client_lifecycle(self, client, sample_intake_data):
        """Test the complete client lifecycle: create, read, update, delete."""
        # This test would require actual database setup in a real scenario
        # For now, we'll mock the entire flow
        
        with patch('backend.api.clients.create_client_from_intake') as mock_create, \
             patch('backend.api.clients.get_client_by_id') as mock_get, \
             patch('backend.api.clients.update_client') as mock_update, \
             patch('backend.api.clients.delete_client') as mock_delete:
            
            # Create client
            created_profile = ClientProfile(**sample_intake_data)
            mock_create.return_value = created_profile
            
            create_response = client.post("/api/clients/intake", json=sample_intake_data)
            assert create_response.status_code == 201
            client_id = create_response.json()["id"]
            
            # Read client
            mock_get.return_value = created_profile
            get_response = client.get(f"/api/clients/{client_id}")
            assert get_response.status_code == 200
            assert get_response.json()["name"] == "John Doe"
            
            # Update client
            updated_profile = created_profile.model_copy()
            updated_profile.name = "John Updated"
            mock_update.return_value = updated_profile
            
            update_response = client.put(f"/api/clients/{client_id}", json={"name": "John Updated"})
            assert update_response.status_code == 200
            assert update_response.json()["name"] == "John Updated"
            
            # Delete client
            mock_delete.return_value = True
            delete_response = client.delete(f"/api/clients/{client_id}")
            assert delete_response.status_code == 204
