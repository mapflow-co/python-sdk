"""
Basic usage examples for MapFlow SDK.

This script demonstrates basic CRUD operations for the main resources.
"""

from mapflow import (
    MapFlowClient,
    CustomerType,
    ItemType,
    VehicleType,
    EnergyType,
    WarehouseType
)

# Initialize client
API_KEY = "your-api-key-here"
client = MapFlowClient(api_key=API_KEY)


def customer_examples():
    """Examples for customer management."""
    print("\n=== Customer Examples ===\n")
    
    # Create a company customer
    customer = client.create_customer({
        "customer_type": CustomerType.COMPANY,
        "company_name": "Acme Corporation",
        "email": "contact@acme.com",
        "phone": "+33123456789",
        "billing_address": "123 rue de la Paix",
        "billing_zip_code": "75001",
        "billing_city": "Paris",
        "billing_country": "FR",
        "siret": "12345678901234",
        "is_active": True
    })
    print(f"Created customer: {customer.display_name} (ID: {customer.id})")
    
    # List customers
    customers = client.list_customers(is_active=True)
    print(f"\nTotal active customers: {customers.count}")
    
    # Get customer details
    customer_detail = client.get_customer(customer.id)
    print(f"\nCustomer details: {customer_detail.display_name}")
    
    # Update customer
    updated_customer = client.patch_customer(customer.id, {
        "notes": "Premier client"
    })
    print(f"\nUpdated customer notes")
    
    return customer.id


def delivery_location_examples(customer_id):
    """Examples for delivery location management."""
    print("\n=== Delivery Location Examples ===\n")
    
    # Create delivery location
    location = client.create_delivery_location({
        "customer": customer_id,
        "name": "Entrepôt Principal",
        "address": "456 avenue des Champs",
        "zip_code": "75008",
        "city": "Paris",
        "country": "FR",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "truck_access": True,
        "loading_dock": True,
        "max_weight_kg": 5000,
        "delivery_instructions": "Livraison côté quai 3",
        "is_active": True
    })
    print(f"Created location: {location.name} (ID: {location.id})")
    
    # List locations
    locations = client.list_delivery_locations(city="Paris")
    print(f"\nLocations in Paris: {locations.count}")
    
    # Get customer locations
    customer_locations = client.get_customer_locations(customer_id)
    print(f"\nCustomer has {len(customer_locations)} location(s)")
    
    return location.id


def warehouse_examples():
    """Examples for warehouse management."""
    print("\n=== Warehouse Examples ===\n")
    
    # Create warehouse
    warehouse = client.create_warehouse({
        "name": "Hub Logistique Paris Nord",
        "code": "PARIS-01",
        "warehouse_type": WarehouseType.HUB,
        "address": "12 rue Industrielle",
        "zip_code": "93200",
        "city": "Saint-Denis",
        "country": "FR",
        "latitude": 48.9356,
        "longitude": 2.3539,
        "opening_time": "08:00:00",
        "closing_time": "18:00:00",
        "is_start_point": True,
        "is_end_point": True,
        "has_loading_dock": True,
        "max_vehicles": 50
    })
    print(f"Created warehouse: {warehouse.name} (ID: {warehouse.id})")
    
    # Set as default
    client.set_default_warehouse(warehouse.id)
    print(f"\nSet {warehouse.name} as default warehouse")
    
    # List warehouses
    warehouses = client.list_warehouses(is_active=True)
    print(f"\nTotal active warehouses: {warehouses.count}")
    
    return warehouse.id


def delivery_item_examples():
    """Examples for delivery item management."""
    print("\n=== Delivery Item Examples ===\n")
    
    # Create product
    item = client.create_delivery_item({
        "name": "Smartphone XYZ",
        "item_type": ItemType.PRODUCT,
        "reference": "PROD-001",
        "weight": 0.2,
        "weight_unit": "kg",
        "length": 15,
        "width": 7,
        "height": 1,
        "is_fragile": True,
        "declared_value": 500.0,
        "currency": "EUR",
        "buying_price": 300.0,
        "selling_price": 500.0,
        "vat_rate": 20.0
    })
    print(f"Created item: {item.name} (ID: {item.id})")
    
    # List items
    items = client.list_delivery_items(item_type=ItemType.PRODUCT)
    print(f"\nTotal products: {items.count}")
    
    # Search fragile items
    fragile_items = client.list_delivery_items(is_fragile=True)
    print(f"\nFragile items: {fragile_items.count}")
    
    return item.id


def vehicle_examples(warehouse_id):
    """Examples for vehicle management."""
    print("\n=== Vehicle Examples ===\n")
    
    # Create vehicle
    vehicle = client.create_vehicle({
        "name": "Fourgon 01",
        "license_plate": "AB-123-CD",
        "vehicle_type": VehicleType.VAN_MEDIUM,
        "brand": "Renault",
        "model": "Master",
        "year": 2023,
        "energy_type": EnergyType.DIESEL,
        "max_weight_kg": 1500,
        "max_volume_m3": 12.0,
        "max_distance_km": 500,
        "status": "available",
        "assigned_warehouses": [str(warehouse_id)]
    })
    print(f"Created vehicle: {vehicle.name} (ID: {vehicle.id})")
    
    # List vehicles
    vehicles = client.list_vehicles(status="available")
    print(f"\nAvailable vehicles: {len(vehicles)}")
    
    return vehicle.id


def tag_examples():
    """Examples for tag management."""
    print("\n=== Tag Examples ===\n")
    
    # Create tag
    tag = client.create_tag({
        "name": "Urgent",
        "color": "#FF0000",
        "description": "Livraisons urgentes"
    })
    print(f"Created tag: {tag.name} (ID: {tag.id})")
    
    # List tags
    tags = client.list_tags()
    print(f"\nTotal tags: {tags.count}")
    
    return tag.id


def bulk_action_examples(customer_ids):
    """Examples for bulk actions."""
    print("\n=== Bulk Action Examples ===\n")
    
    # Bulk activate customers
    result = client.customer_bulk_action(
        action="activate",
        customer_ids=customer_ids
    )
    print(f"Bulk action result: {result}")


def main():
    """Run all examples."""
    try:
        # Customer management
        customer_id = customer_examples()
        
        # Delivery location management
        location_id = delivery_location_examples(customer_id)
        
        # Warehouse management
        warehouse_id = warehouse_examples()
        
        # Delivery item management
        item_id = delivery_item_examples()
        
        # Vehicle management
        vehicle_id = vehicle_examples(warehouse_id)
        
        # Tag management
        tag_id = tag_examples()
        
        # Bulk actions
        bulk_action_examples([customer_id])
        
        print("\n=== All examples completed successfully! ===\n")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

