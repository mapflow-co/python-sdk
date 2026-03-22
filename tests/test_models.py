"""Tests for Pydantic models."""

import unittest
from datetime import datetime, date
from uuid import UUID, uuid4

from pydantic import ValidationError

from mapflow.models import (
    Customer,
    CustomerCreate,
    DeliveryLocation,
    DeliveryLocationCreate,
    Warehouse,
    WarehouseCreate,
    DeliveryItem,
    DeliveryItemCreate,
    Vehicle,
    VehicleCreate,
    Tag,
    TagCreate
)
from mapflow.constants import (
    CustomerType,
    ItemType,
    VehicleType,
    WarehouseType
)


class TestCustomerModels(unittest.TestCase):
    """Test customer models."""
    
    def test_customer_create_valid(self):
        """Test creating valid customer."""
        customer = CustomerCreate(
            customer_type=CustomerType.COMPANY,
            company_name="Test Corp",
            billing_city="Paris",
            is_active=True
        )
        
        self.assertEqual(customer.customer_type, CustomerType.COMPANY)
        self.assertEqual(customer.company_name, "Test Corp")
        self.assertTrue(customer.is_active)
    
    def test_customer_create_individual(self):
        """Test creating individual customer."""
        customer = CustomerCreate(
            customer_type=CustomerType.INDIVIDUAL,
            first_name="John",
            last_name="Doe",
            email="john@example.com"
        )
        
        self.assertEqual(customer.customer_type, CustomerType.INDIVIDUAL)
        self.assertEqual(customer.first_name, "John")
    
    def test_customer_with_lists(self):
        """Test customer with email/phone lists."""
        customer = CustomerCreate(
            customer_type=CustomerType.COMPANY,
            company_name="Test",
            emails=["test1@example.com", "test2@example.com"],
            phones=["+33123456789", "+33987654321"]
        )
        
        self.assertEqual(len(customer.emails), 2)
        self.assertEqual(len(customer.phones), 2)
    
    def test_customer_model_dump(self):
        """Test customer model serialization."""
        customer = CustomerCreate(
            customer_type=CustomerType.COMPANY,
            company_name="Test Corp"
        )
        
        data = customer.model_dump(exclude_none=True)
        
        self.assertIn('customer_type', data)
        self.assertIn('company_name', data)
        self.assertEqual(data['customer_type'], 'company')


class TestDeliveryLocationModels(unittest.TestCase):
    """Test delivery location models."""
    
    def test_delivery_location_create_valid(self):
        """Test creating valid delivery location."""
        customer_id = uuid4()
        location = DeliveryLocationCreate(
            customer=customer_id,
            name="Test Location",
            address="123 Test St",
            zip_code="75001",
            city="Paris",
            country="FR"
        )
        
        self.assertEqual(location.customer, customer_id)
        self.assertEqual(location.name, "Test Location")
        self.assertEqual(location.city, "Paris")
    
    def test_delivery_location_with_coordinates(self):
        """Test location with GPS coordinates."""
        location = DeliveryLocationCreate(
            customer=uuid4(),
            name="Test",
            address="123 Test St",
            zip_code="75001",
            city="Paris",
            latitude=48.8566,
            longitude=2.3522
        )
        
        self.assertIsNotNone(location.latitude)
        self.assertIsNotNone(location.longitude)
    
    def test_delivery_location_with_constraints(self):
        """Test location with physical constraints."""
        location = DeliveryLocationCreate(
            customer=uuid4(),
            name="Test",
            address="123 Test St",
            zip_code="75001",
            city="Paris",
            truck_access=True,
            loading_dock=True,
            elevator_access=False,
            max_weight_kg=5000
        )
        
        self.assertTrue(location.truck_access)
        self.assertTrue(location.loading_dock)
        self.assertEqual(location.max_weight_kg, 5000)


class TestWarehouseModels(unittest.TestCase):
    """Test warehouse models."""
    
    def test_warehouse_create_valid(self):
        """Test creating valid warehouse."""
        warehouse = WarehouseCreate(
            name="Test Warehouse",
            code="TEST-01",
            warehouse_type=WarehouseType.HUB,
            address="123 Test St",
            zip_code="75001",
            city="Paris"
        )
        
        self.assertEqual(warehouse.name, "Test Warehouse")
        self.assertEqual(warehouse.warehouse_type, WarehouseType.HUB)
    
    def test_warehouse_with_hours(self):
        """Test warehouse with opening hours."""
        warehouse = WarehouseCreate(
            name="Test Warehouse",
            address="123 Test St",
            zip_code="75001",
            city="Paris",
            opening_time="08:00:00",
            closing_time="18:00:00"
        )
        
        self.assertIsNotNone(warehouse.opening_time)
        self.assertIsNotNone(warehouse.closing_time)


class TestDeliveryItemModels(unittest.TestCase):
    """Test delivery item models."""
    
    def test_delivery_item_create_valid(self):
        """Test creating valid delivery item."""
        item = DeliveryItemCreate(
            name="Test Product",
            item_type=ItemType.PRODUCT,
            weight=1.5,
            weight_unit="kg",
            is_fragile=True
        )
        
        self.assertEqual(item.name, "Test Product")
        self.assertEqual(item.item_type, ItemType.PRODUCT)
        self.assertTrue(item.is_fragile)
    
    def test_delivery_item_with_dimensions(self):
        """Test item with dimensions."""
        item = DeliveryItemCreate(
            name="Box",
            item_type=ItemType.PACKAGE,
            length=50,
            width=30,
            height=20,
            weight=2.5
        )
        
        self.assertEqual(item.length, 50)
        self.assertEqual(item.width, 30)
        self.assertEqual(item.height, 20)
    
    def test_delivery_item_with_price(self):
        """Test item with pricing."""
        item = DeliveryItemCreate(
            name="Product",
            item_type=ItemType.PRODUCT,
            buying_price=100.0,
            selling_price=150.0,
            vat_rate=20.0,
            currency="EUR"
        )
        
        self.assertEqual(item.buying_price, 100.0)
        self.assertEqual(item.selling_price, 150.0)
        self.assertEqual(item.vat_rate, 20.0)


class TestVehicleModels(unittest.TestCase):
    """Test vehicle models."""
    
    def test_vehicle_create_valid(self):
        """Test creating valid vehicle."""
        vehicle = VehicleCreate(
            name="Test Van",
            license_plate="AB-123-CD",
            vehicle_type=VehicleType.VAN_MEDIUM
        )
        
        self.assertEqual(vehicle.name, "Test Van")
        self.assertEqual(vehicle.license_plate, "AB-123-CD")
        self.assertEqual(vehicle.vehicle_type, VehicleType.VAN_MEDIUM)
    
    def test_vehicle_with_capacity(self):
        """Test vehicle with capacity information."""
        vehicle = VehicleCreate(
            name="Truck",
            license_plate="XY-789-ZZ",
            vehicle_type=VehicleType.TRUCK_SMALL,
            max_weight_kg=3500,
            max_volume_m3=20.0,
            max_distance_km=500
        )
        
        self.assertEqual(vehicle.max_weight_kg, 3500)
        self.assertEqual(vehicle.max_volume_m3, 20.0)
        self.assertEqual(vehicle.max_distance_km, 500)


class TestTagModels(unittest.TestCase):
    """Test tag models."""
    
    def test_tag_create_valid(self):
        """Test creating valid tag."""
        tag = TagCreate(
            name="Urgent",
            color="#FF0000"
        )
        
        self.assertEqual(tag.name, "Urgent")
        self.assertEqual(tag.color, "#FF0000")
    
    def test_tag_invalid_color(self):
        """Test tag with invalid color format."""
        with self.assertRaises(ValidationError):
            TagCreate(
                name="Test",
                color="red"  # Invalid format
            )
    
    def test_tag_with_description(self):
        """Test tag with description."""
        tag = TagCreate(
            name="VIP",
            color="#FFD700",
            description="VIP customers"
        )
        
        self.assertEqual(tag.description, "VIP customers")


class TestModelSerialization(unittest.TestCase):
    """Test model serialization."""
    
    def test_model_dump_exclude_none(self):
        """Test excluding None values in serialization."""
        customer = CustomerCreate(
            customer_type=CustomerType.COMPANY,
            company_name="Test",
            email=None,
            phone=None
        )
        
        data = customer.model_dump(exclude_none=True)
        
        self.assertNotIn('email', data)
        self.assertNotIn('phone', data)
        self.assertIn('company_name', data)
    
    def test_enum_serialization(self):
        """Test enum value serialization."""
        item = DeliveryItemCreate(
            name="Test",
            item_type=ItemType.PRODUCT
        )
        
        data = item.model_dump()
        
        # Enums should be serialized as their string values
        self.assertEqual(data['item_type'], 'PRODUCT')


if __name__ == '__main__':
    unittest.main()

