"""
Validation example using Pydantic models.

This example demonstrates how to use Pydantic models for data validation
before sending requests to the API.
"""

from pydantic import ValidationError as PydanticValidationError
from mapflow import (
    MapFlowClient,
    CustomerCreate,
    CustomerType,
    DeliveryItemCreate,
    ItemType,
    VehicleCreate,
    VehicleType,
    TagCreate
)


def validate_customer_data():
    """Demonstrate customer data validation."""
    print("\n=== Customer Data Validation ===\n")
    
    # Valid customer
    try:
        customer = CustomerCreate(
            customer_type=CustomerType.COMPANY,
            company_name="Valid Company",
            email="valid@example.com",
            billing_country="FR"
        )
        print("✓ Valid customer data:")
        print(f"  Company: {customer.company_name}")
        print(f"  Type: {customer.customer_type}")
        
        # Convert to dict for API
        customer_dict = customer.model_dump(exclude_none=True)
        print(f"  Serialized fields: {len(customer_dict)}")
        
    except PydanticValidationError as e:
        print(f"✗ Validation error: {e}")
    
    # Invalid customer - missing required field for company type
    print("\n2. Testing invalid customer data...")
    try:
        invalid_customer = CustomerCreate(
            customer_type=CustomerType.COMPANY,
            # Missing company_name for company type
            email="test@example.com"
        )
        # This might not fail at model level but could fail at API level
        print("  Model created (API might reject it)")
    except PydanticValidationError as e:
        print(f"✗ Validation error: {e}")


def validate_delivery_item_data():
    """Demonstrate delivery item validation."""
    print("\n=== Delivery Item Validation ===\n")
    
    # Valid item
    try:
        item = DeliveryItemCreate(
            name="Laptop",
            item_type=ItemType.PRODUCT,
            weight=2.5,
            weight_unit="kg",
            length=35,
            width=25,
            height=3,
            is_fragile=True,
            declared_value=1000.0,
            currency="EUR"
        )
        print("✓ Valid delivery item:")
        print(f"  Name: {item.name}")
        print(f"  Type: {item.item_type}")
        print(f"  Weight: {item.weight} {item.weight_unit}")
        print(f"  Dimensions: {item.length}x{item.width}x{item.height} cm")
        
    except PydanticValidationError as e:
        print(f"✗ Validation error: {e}")
    
    # Item without required fields
    print("\n2. Testing item without required name...")
    try:
        invalid_item = DeliveryItemCreate(
            item_type=ItemType.PRODUCT,
            # Missing name (required)
        )
    except PydanticValidationError as e:
        print(f"✗ Validation error caught: Field 'name' is required")


def validate_vehicle_data():
    """Demonstrate vehicle validation."""
    print("\n=== Vehicle Validation ===\n")
    
    # Valid vehicle
    try:
        vehicle = VehicleCreate(
            name="Delivery Van",
            license_plate="AB-123-CD",
            vehicle_type=VehicleType.VAN_MEDIUM,
            brand="Renault",
            model="Master",
            year=2023,
            max_weight_kg=1500,
            max_volume_m3=12.0
        )
        print("✓ Valid vehicle:")
        print(f"  Name: {vehicle.name}")
        print(f"  License: {vehicle.license_plate}")
        print(f"  Type: {vehicle.vehicle_type}")
        print(f"  Capacity: {vehicle.max_weight_kg}kg, {vehicle.max_volume_m3}m³")
        
    except PydanticValidationError as e:
        print(f"✗ Validation error: {e}")


def validate_tag_data():
    """Demonstrate tag validation."""
    print("\n=== Tag Validation ===\n")
    
    # Valid tag
    try:
        tag = TagCreate(
            name="Urgent",
            color="#FF0000",
            description="Urgent deliveries"
        )
        print("✓ Valid tag:")
        print(f"  Name: {tag.name}")
        print(f"  Color: {tag.color}")
        
    except PydanticValidationError as e:
        print(f"✗ Validation error: {e}")
    
    # Invalid color format
    print("\n2. Testing invalid color format...")
    try:
        invalid_tag = TagCreate(
            name="Test",
            color="red"  # Invalid: must be hex format like #FF0000
        )
    except PydanticValidationError as e:
        print(f"✗ Validation error caught: Color must be hex format (#RRGGBB)")


def demonstrate_model_serialization():
    """Demonstrate model serialization features."""
    print("\n=== Model Serialization ===\n")
    
    # Create customer with some optional fields
    customer = CustomerCreate(
        customer_type=CustomerType.COMPANY,
        company_name="Serialization Demo",
        email="demo@example.com",
        billing_city="Paris",
        # Some fields intentionally None
        phone=None,
        notes=None
    )
    
    # Serialize with None values
    full_dict = customer.model_dump()
    print(f"1. Full serialization (with None): {len(full_dict)} fields")
    print(f"   Keys: {list(full_dict.keys())[:5]}...")
    
    # Serialize excluding None values (recommended for API)
    clean_dict = customer.model_dump(exclude_none=True)
    print(f"\n2. Clean serialization (exclude None): {len(clean_dict)} fields")
    print(f"   Keys: {list(clean_dict.keys())}")
    
    # Show the difference
    print(f"\n3. Difference: {len(full_dict) - len(clean_dict)} None fields excluded")


def validate_with_api(client):
    """Validate data with actual API calls."""
    print("\n=== Validation with API ===\n")
    
    print("Testing Global Customer validation endpoint...")
    
    # Prepare test data
    test_data = {
        "customer_type": CustomerType.COMPANY,
        "company_name": "Validation Test Corp",
        "delivery_location": {
            "name": "Test Location",
            "address": "123 Test Street",
            "zip_code": "75001",
            "city": "Paris",
            "country": "FR"
        }
    }
    
    try:
        result = client.validate_global_customer_data(test_data)
        
        if result.get('valid'):
            print("✓ Data is valid!")
            print(f"  Message: {result.get('message')}")
        else:
            print("✗ Data is invalid:")
            print(f"  Errors: {result.get('errors')}")
            
    except MapFlowError as e:
        print(f"✗ API Error: {e.message}")


def main():
    """Run validation examples."""
    print("="*60)
    print("MapFlow SDK - Validation Examples")
    print("="*60)
    
    # Get API key
    api_key = get_api_key()
    
    # Initialize client
    client = MapFlowClient(api_key=api_key)
    
    # Run local validation examples
    validate_customer_data()
    validate_delivery_item_data()
    validate_vehicle_data()
    validate_tag_data()
    demonstrate_model_serialization()
    
    # Test with API
    print("\n\nDo you want to test validation with the real API? (y/n): ", end="")
    if input().strip().lower() == 'y':
        validate_with_api(client)
    
    print("\n" + "="*60)
    print("Validation examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()

