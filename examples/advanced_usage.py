"""
Advanced usage examples for MapFlow SDK.

This script demonstrates advanced features like bulk operations,
global customers, error handling, and complex queries.
"""

from mapflow import (
    MapFlowClient,
    CustomerType,
    MapFlowError,
    AuthenticationError,
    NotFoundError,
    ValidationError
)

# Initialize client
API_KEY = "your-api-key-here"
client = MapFlowClient(api_key=API_KEY)


def error_handling_example():
    """Demonstrate proper error handling."""
    print("\n=== Error Handling Examples ===\n")
    
    try:
        # Try to get non-existent customer
        customer = client.get_customer("00000000-0000-0000-0000-000000000000")
    except NotFoundError as e:
        print(f"Customer not found: {e.message}")
    except MapFlowError as e:
        print(f"API error: {e.message}")
    
    try:
        # Try to create invalid customer
        customer = client.create_customer({
            "customer_type": "invalid_type",  # Invalid!
            "company_name": "Test"
        })
    except ValidationError as e:
        print(f"Validation error: {e.message}")
        print(f"Details: {e.response}")


def global_customer_example():
    """Demonstrate global customer API (atomic creation)."""
    print("\n=== Global Customer Example ===\n")
    
    # Create complete customer in one call
    global_customer = client.create_global_customer({
        "customer_type": CustomerType.COMPANY,
        "company_name": "Tech Solutions SARL",
        "email": "contact@techsolutions.fr",
        "phone": "+33123456789",
        "billing_address": "50 rue Innovation",
        "billing_zip_code": "69001",
        "billing_city": "Lyon",
        "billing_country": "FR",
        "siret": "98765432109876",
        "delivery_location": {
            "name": "Bureau Principal",
            "address": "10 rue de la Tech",
            "zip_code": "69001",
            "city": "Lyon",
            "country": "FR",
            "latitude": 45.764043,
            "longitude": 4.835659,
            "truck_access": True,
            "loading_dock": False
        },
        "contact": {
            "first_name": "Marie",
            "last_name": "Martin",
            "position": "Responsable Logistique",
            "emails": ["marie.martin@techsolutions.fr"],
            "phones": ["+33123456789"],
            "is_primary": True
        },
        "opening_hours": [
            {
                "day_of_week": 0,  # Monday
                "opening_time": "09:00:00",
                "closing_time": "18:00:00"
            },
            {
                "day_of_week": 1,  # Tuesday
                "opening_time": "09:00:00",
                "closing_time": "18:00:00"
            },
            {
                "day_of_week": 2,  # Wednesday
                "opening_time": "09:00:00",
                "closing_time": "18:00:00"
            },
            {
                "day_of_week": 3,  # Thursday
                "opening_time": "09:00:00",
                "closing_time": "18:00:00"
            },
            {
                "day_of_week": 4,  # Friday
                "opening_time": "09:00:00",
                "closing_time": "17:00:00"
            }
        ]
    })
    
    print(f"Created global customer: {global_customer.display_name}")
    print(f"ID: {global_customer.id}")
    
    return global_customer.id


def bulk_operations_example():
    """Demonstrate bulk operations."""
    print("\n=== Bulk Operations Examples ===\n")
    
    # Create multiple customers
    customer_ids = []
    for i in range(3):
        customer = client.create_customer({
            "customer_type": CustomerType.INDIVIDUAL,
            "first_name": f"User{i}",
            "last_name": f"Test{i}",
            "email": f"user{i}@test.com",
            "billing_city": "Paris",
            "is_active": False
        })
        customer_ids.append(str(customer.id))
        print(f"Created customer {i+1}: {customer.display_name}")
    
    # Bulk activate
    print("\nActivating customers in bulk...")
    result = client.customer_bulk_action(
        action="activate",
        customer_ids=customer_ids
    )
    print(f"Bulk activation result: {result}")
    
    # Create tags
    tag1 = client.create_tag({
        "name": "VIP",
        "color": "#FFD700",
        "description": "VIP customers"
    })
    tag2 = client.create_tag({
        "name": "Premium",
        "color": "#C0C0C0",
        "description": "Premium customers"
    })
    
    # Bulk add tags
    print("\nAdding tags in bulk...")
    result = client.customer_bulk_action(
        action="add_tags",
        customer_ids=customer_ids,
        tag_ids=[str(tag1.id), str(tag2.id)]
    )
    print(f"Bulk tag assignment result: {result}")
    
    return customer_ids


def advanced_search_example():
    """Demonstrate advanced search and filtering."""
    print("\n=== Advanced Search Examples ===\n")
    
    # Complex customer search
    customers = client.list_customers(
        search="Tech",
        customer_type=CustomerType.COMPANY,
        is_active=True,
        has_locations=True,
        min_locations=1
    )
    print(f"Found {customers.count} company customers with 'Tech' in name")
    
    # Advanced delivery location filtering
    locations = client.list_delivery_locations(
        city="Paris",
        has_coordinates=True,
        truck_access=True,
        loading_dock=True,
        is_active=True
    )
    print(f"\nFound {locations.count} Paris locations with truck access")
    
    # Complex product search
    items = client.list_delivery_items(
        item_type="PRODUCT",
        is_fragile=True,
        weight_min=0.1,
        weight_max=5.0,
        declared_value_min=100,
        has_tags=True
    )
    print(f"\nFound {items.count} fragile products between 0.1-5kg worth >100€")


def pagination_example():
    """Demonstrate pagination handling."""
    print("\n=== Pagination Example ===\n")
    
    page = 1
    total_processed = 0
    
    while True:
        # Get page
        response = client.list_customers(page=page)
        
        print(f"Processing page {page} ({len(response.results)} items)")
        
        # Process customers
        for customer in response.results:
            total_processed += 1
            print(f"  - {customer.display_name}")
        
        # Check if there's a next page
        if not response.next:
            break
        
        page += 1
    
    print(f"\nTotal processed: {total_processed} customers")


def contact_and_opening_hours_example():
    """Demonstrate contacts and opening hours management."""
    print("\n=== Contacts & Opening Hours Examples ===\n")
    
    # Create customer and location first
    customer = client.create_customer({
        "customer_type": CustomerType.COMPANY,
        "company_name": "Contact Test Corp",
        "billing_city": "Lyon"
    })
    
    location = client.create_delivery_location({
        "customer": customer.id,
        "name": "Test Location",
        "address": "123 Test Street",
        "zip_code": "69001",
        "city": "Lyon",
        "country": "FR"
    })
    
    # Create contact
    contact = client.create_contact({
        "first_name": "Jean",
        "last_name": "Dupont",
        "position": "Manager",
        "emails": ["jean.dupont@test.com", "j.dupont@test.com"],
        "phones": ["+33123456789", "+33987654321"],
        "is_primary": True,
        "location_ids": [str(location.id)]
    })
    print(f"Created contact: {contact.full_name}")
    
    # Create opening hours for each weekday
    for day in range(5):  # Monday to Friday
        hours = client.create_opening_hours({
            "location": location.id,
            "day_of_week": day,
            "opening_time": "09:00:00",
            "closing_time": "18:00:00",
            "break_start": "12:00:00",
            "break_end": "13:00:00"
        })
        print(f"Created opening hours for day {day}")
    
    # List location contacts
    contacts = client.list_contacts(location=str(location.id))
    print(f"\nLocation has {contacts.count} contact(s)")
    
    # List location opening hours
    hours = client.list_opening_hours(location=str(location.id))
    print(f"Location has {hours.count} opening hour(s)")


def driver_and_vehicle_example():
    """Demonstrate driver and vehicle management."""
    print("\n=== Driver & Vehicle Management ===\n")
    
    # Create warehouse first
    warehouse = client.create_warehouse({
        "name": "Test Warehouse",
        "code": "TEST-01",
        "address": "1 Test Ave",
        "zip_code": "75001",
        "city": "Paris",
        "country": "FR"
    })
    
    # Create driver
    driver = client.create_driver_picker({
        "email": "driver@test.com",
        "first_name": "Pierre",
        "last_name": "Chauffeur",
        "phone": "+33123456789",
        "role": "driver",
        "employee_id": "DRV-001",
        "password": "SecurePass123!",
        "confirm_password": "SecurePass123!",
        "has_valid_driving_license": True,
        "driver_license_number": "ABC123456",
        "driver_licence_type": ["b", "c"],
        "vehicle_types": ["van_medium", "truck_small"]
    })
    print(f"Created driver: {driver.full_name}")
    
    # Create vehicle
    vehicle = client.create_vehicle({
        "name": "Camion 01",
        "license_plate": "XY-789-ZZ",
        "vehicle_type": "truck_small",
        "brand": "Mercedes",
        "model": "Sprinter",
        "year": 2022,
        "energy_type": "diesel",
        "max_weight_kg": 3500,
        "max_volume_m3": 20.0,
        "status": "available",
        "assigned_warehouses": [str(warehouse.id)]
    })
    print(f"Created vehicle: {vehicle.name}")
    
    # Update vehicle status
    client.patch_vehicle(vehicle.id, {
        "status": "in_use",
        "current_km": 50000
    })
    print(f"Updated vehicle status to in_use")


def main():
    """Run all advanced examples."""
    try:
        # Error handling
        error_handling_example()
        
        # Global customer (atomic creation)
        global_customer_id = global_customer_example()
        
        # Bulk operations
        customer_ids = bulk_operations_example()
        
        # Advanced search
        advanced_search_example()
        
        # Pagination
        pagination_example()
        
        # Contacts and opening hours
        contact_and_opening_hours_example()
        
        # Driver and vehicle management
        driver_and_vehicle_example()
        
        print("\n=== All advanced examples completed successfully! ===\n")
        
    except MapFlowError as e:
        print(f"\nMapFlow API Error: {e.message}")
        if e.response:
            print(f"Response: {e.response}")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

