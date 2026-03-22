"""Basic tests for MapFlow client."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from uuid import UUID

from mapflow import (
    MapFlowClient,
    Customer,
    DeliveryLocation,
    Warehouse,
    DeliveryItem,
    Vehicle,
    Tag,
    AuthenticationError,
    NotFoundError,
    ValidationError
)


class TestMapFlowClient(unittest.TestCase):
    """Test MapFlow client initialization and basic methods."""
    
    def setUp(self):
        """Set up test client."""
        self.api_key = "test-api-key"
        self.client = MapFlowClient(api_key=self.api_key)
    
    def test_client_initialization(self):
        """Test client initialization."""
        self.assertEqual(self.client.api_key, self.api_key)
        self.assertEqual(self.client.base_url, "https://api.mapflow.co")
        self.assertEqual(self.client.timeout, 30)
        self.assertIn('X-API-Key', self.client.session.headers)
        self.assertEqual(self.client.session.headers['X-API-Key'], self.api_key)
    
    def test_client_custom_base_url(self):
        """Test client with custom base URL."""
        custom_url = "https://api-test.mapflow.co"
        client = MapFlowClient(api_key=self.api_key, base_url=custom_url)
        self.assertEqual(client.base_url, custom_url)
    
    @patch('mapflow.client.requests.Session.request')
    def test_handle_response_200(self, mock_request):
        """Test successful response handling."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "123", "name": "Test"}
        mock_request.return_value = mock_response
        
        result = self.client._request('GET', '/test/')
        self.assertEqual(result, {"id": "123", "name": "Test"})
    
    @patch('mapflow.client.requests.Session.request')
    def test_handle_response_401(self, mock_request):
        """Test authentication error handling."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"detail": "Invalid API key"}
        mock_request.return_value = mock_response
        
        with self.assertRaises(AuthenticationError) as context:
            self.client._request('GET', '/test/')
        
        self.assertEqual(context.exception.status_code, 401)
    
    @patch('mapflow.client.requests.Session.request')
    def test_handle_response_404(self, mock_request):
        """Test not found error handling."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"detail": "Not found"}
        mock_request.return_value = mock_response
        
        with self.assertRaises(NotFoundError) as context:
            self.client._request('GET', '/test/')
        
        self.assertEqual(context.exception.status_code, 404)
    
    @patch('mapflow.client.requests.Session.request')
    def test_handle_response_400(self, mock_request):
        """Test validation error handling."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"detail": "Validation error"}
        mock_request.return_value = mock_response
        
        with self.assertRaises(ValidationError) as context:
            self.client._request('GET', '/test/')
        
        self.assertEqual(context.exception.status_code, 400)


class TestCustomerMethods(unittest.TestCase):
    """Test customer-related methods."""
    
    def setUp(self):
        """Set up test client."""
        self.client = MapFlowClient(api_key="test-api-key")
    
    @patch('mapflow.client.requests.Session.request')
    def test_list_customers(self, mock_request):
        """Test listing customers."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "customer_type": "company",
                    "company_name": "Test Corp",
                    "organisation": "123e4567-e89b-12d3-a456-426614174001",
                    "is_active": True,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z"
                }
            ]
        }
        mock_request.return_value = mock_response
        
        result = self.client.list_customers()
        
        self.assertEqual(result.count, 1)
        self.assertEqual(len(result.results), 1)
        mock_request.assert_called_once()
    
    @patch('mapflow.client.requests.Session.request')
    def test_create_customer(self, mock_request):
        """Test creating a customer."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "customer_type": "company",
            "company_name": "New Corp",
            "organisation": "123e4567-e89b-12d3-a456-426614174001",
            "is_active": True,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        mock_request.return_value = mock_response
        
        customer_data = {
            "customer_type": "company",
            "company_name": "New Corp"
        }
        
        result = self.client.create_customer(customer_data)
        
        self.assertIsInstance(result, Customer)
        self.assertEqual(result.company_name, "New Corp")
        # Verify request was called
        self.assertTrue(mock_request.called)
    
    @patch('mapflow.client.requests.Session.request')
    def test_get_customer(self, mock_request):
        """Test getting a customer."""
        customer_id = "123e4567-e89b-12d3-a456-426614174000"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": customer_id,
            "customer_type": "company",
            "company_name": "Test Corp",
            "organisation": "123e4567-e89b-12d3-a456-426614174001",
            "is_active": True,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        mock_request.return_value = mock_response
        
        result = self.client.get_customer(customer_id)
        
        self.assertIsInstance(result, Customer)
        self.assertEqual(str(result.id), customer_id)
        mock_request.assert_called_once()


class TestDeliveryLocationMethods(unittest.TestCase):
    """Test delivery location methods."""
    
    def setUp(self):
        """Set up test client."""
        self.client = MapFlowClient(api_key="test-api-key")
    
    @patch('mapflow.client.requests.Session.request')
    def test_list_delivery_locations(self, mock_request):
        """Test listing delivery locations."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "customer": "123e4567-e89b-12d3-a456-426614174001",
                    "name": "Test Location",
                    "address": "123 Test St",
                    "zip_code": "75001",
                    "city": "Paris",
                    "is_active": True,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z"
                }
            ]
        }
        mock_request.return_value = mock_response
        
        result = self.client.list_delivery_locations()
        
        self.assertEqual(result.count, 1)
        mock_request.assert_called_once()


class TestWarehouseMethods(unittest.TestCase):
    """Test warehouse methods."""
    
    def setUp(self):
        """Set up test client."""
        self.client = MapFlowClient(api_key="test-api-key")
    
    @patch('mapflow.client.requests.Session.request')
    def test_list_warehouses(self, mock_request):
        """Test listing warehouses."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "organisation": "123e4567-e89b-12d3-a456-426614174001",
                    "name": "Test Warehouse",
                    "code": "TEST-01",
                    "address": "123 Test St",
                    "zip_code": "75001",
                    "city": "Paris",
                    "is_active": True,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z"
                }
            ]
        }
        mock_request.return_value = mock_response
        
        result = self.client.list_warehouses()
        
        self.assertEqual(result.count, 1)
        mock_request.assert_called_once()


class TestVehicleMethods(unittest.TestCase):
    """Test vehicle methods."""
    
    def setUp(self):
        """Set up test client."""
        self.client = MapFlowClient(api_key="test-api-key")
    
    @patch('mapflow.client.requests.Session.request')
    def test_list_vehicles(self, mock_request):
        """Test listing vehicles."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "organisation": "123e4567-e89b-12d3-a456-426614174001",
                "name": "Test Vehicle",
                "license_plate": "AB-123-CD",
                "vehicle_type": "van_medium",
                "is_available": True,
                "is_operational": True,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        ]
        mock_request.return_value = mock_response
        
        result = self.client.list_vehicles()
        
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Vehicle)
        mock_request.assert_called_once()


if __name__ == '__main__':
    unittest.main()

