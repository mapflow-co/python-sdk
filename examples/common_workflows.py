"""
Common workflows with MapFlow SDK.

This file demonstrates typical workflows and patterns when using the SDK.
"""

from mapflow import (
    MapFlowClient,
    CustomerType,
    ItemType,
    VehicleType,
    WarehouseType,
    NotFoundError
)


# Initialize client
API_KEY = "your-api-key-here"
client = MapFlowClient(api_key=API_KEY)


def workflow_onboard_new_customer():
    """
    Complete workflow for onboarding a new customer.
    
    Steps:
    1. Create customer
    2. Add delivery location
    3. Add contact
    4. Set up opening hours
    """
    print("\n=== Workflow: Onboard New Customer ===\n")
    
    # Step 1: Create customer
    print("Step 1: Creating customer...")
    customer = client.create_customer({
        "customer_type": CustomerType.COMPANY,
        "company_name": "New Client SARL",
        "email": "contact@newclient.fr",
        "phone": "+33123456789",
        "billing_address": "10 rue Commerce",
        "billing_zip_code": "69001",
        "billing_city": "Lyon",
        "billing_country": "FR",
        "siret": "12345678901234"
    })
    print(f"✓ Customer created: {customer.display_name}")
    
    # Step 2: Add delivery location
    print("\nStep 2: Creating delivery location...")
    location = client.create_delivery_location({
        "customer": customer.id,
        "name": "Entrepôt Principal",
        "address": "50 boulevard Industriel",
        "zip_code": "69200",
        "city": "Vénissieux",
        "country": "FR",
        "latitude": 45.6975,
        "longitude": 4.8872,
        "truck_access": True,
        "loading_dock": True
    })
    print(f"✓ Location created: {location.name}")
    
    # Step 3: Add contact
    print("\nStep 3: Creating contact...")
    contact = client.create_contact({
        "first_name": "Marie",
        "last_name": "Dupont",
        "position": "Responsable Logistique",
        "emails": ["marie.dupont@newclient.fr"],
        "phones": ["+33123456789"],
        "is_primary": True,
        "location_ids": [str(location.id)]
    })
    print(f"✓ Contact created: {contact.full_name}")
    
    # Step 4: Set up opening hours (Monday to Friday)
    print("\nStep 4: Setting up opening hours...")
    for day in range(5):  # 0=Monday to 4=Friday
        hours = client.create_opening_hours({
            "location": location.id,
            "day_of_week": day,
            "opening_time": "09:00:00",
            "closing_time": "18:00:00",
            "break_start": "12:00:00",
            "break_end": "13:00:00"
        })
    print(f"✓ Opening hours created for weekdays")
    
    print("\n✓ Customer onboarding complete!")
    return customer.id, location.id


def workflow_setup_fleet():
    """
    Workflow for setting up vehicle fleet.
    
    Steps:
    1. Create warehouse
    2. Add vehicles
    3. Create tags for fleet management
    4. Assign tags to vehicles
    """
    print("\n=== Workflow: Setup Vehicle Fleet ===\n")
    
    # Step 1: Create warehouse
    print("Step 1: Creating warehouse...")
    warehouse = client.create_warehouse({
        "name": "Fleet Hub",
        "code": "FLEET-01",
        "warehouse_type": WarehouseType.HUB,
        "address": "100 rue Logistique",
        "zip_code": "93200",
        "city": "Saint-Denis",
        "country": "FR",
        "latitude": 48.9356,
        "longitude": 2.3539,
        "is_start_point": True,
        "is_end_point": True
    })
    print(f"✓ Warehouse created: {warehouse.name}")
    
    # Step 2: Add vehicles
    print("\nStep 2: Adding vehicles to fleet...")
    vehicles = []
    
    vehicle_specs = [
        {"name": "Van 01", "plate": "AB-111-CD", "type": VehicleType.VAN_SMALL},
        {"name": "Van 02", "plate": "AB-222-CD", "type": VehicleType.VAN_MEDIUM},
        {"name": "Truck 01", "plate": "AB-333-CD", "type": VehicleType.TRUCK_SMALL}
    ]
    
    for spec in vehicle_specs:
        vehicle = client.create_vehicle({
            "name": spec["name"],
            "license_plate": spec["plate"],
            "vehicle_type": spec["type"],
            "status": "available",
            "assigned_warehouses": [str(warehouse.id)]
        })
        vehicles.append(vehicle)
        print(f"✓ Vehicle created: {vehicle.name}")
    
    # Step 3: Create fleet tags
    print("\nStep 3: Creating fleet tags...")
    tag_cold = client.create_tag({
        "name": "Cold Chain",
        "color": "#00BFFF"
    })
    tag_express = client.create_tag({
        "name": "Express",
        "color": "#FF4500"
    })
    print(f"✓ Tags created")
    
    # Step 4: Tag vehicles
    print("\nStep 4: Assigning tags to vehicles...")
    for vehicle in vehicles[:2]:  # Tag first 2 vehicles as express
        client._request('POST', f'/vehicles/vehicles/{vehicle.id}/manage_tags/', json={
            "object_ids": [str(vehicle.id)],
            "tag_ids": [str(tag_express.id)],
            "action": "add"
        })
    print(f"✓ Tags assigned to vehicles")
    
    print("\n✓ Fleet setup complete!")
    return warehouse.id, [str(v.id) for v in vehicles]


def workflow_organize_catalog():
    """
    Workflow for organizing product catalog with tags.
    
    Steps:
    1. Create product categories as tags
    2. Import products
    3. Assign tags to products
    """
    print("\n=== Workflow: Organize Product Catalog ===\n")
    
    # Step 1: Create category tags
    print("Step 1: Creating category tags...")
    categories = {
        "Electronics": "#1E90FF",
        "Furniture": "#8B4513",
        "Food": "#32CD32",
        "Fragile": "#FF6347"
    }
    
    tag_ids = {}
    for name, color in categories.items():
        tag = client.create_tag({
            "name": name,
            "color": color,
            "description": f"Category: {name}"
        })
        tag_ids[name] = str(tag.id)
        print(f"✓ Created tag: {name}")
    
    # Step 2: Import products
    print("\nStep 2: Importing products...")
    products = [
        {
            "name": "Laptop Professional",
            "type": ItemType.PRODUCT,
            "reference": "ELEC-001",
            "weight": 2.5,
            "is_fragile": True,
            "categories": ["Electronics", "Fragile"]
        },
        {
            "name": "Office Chair",
            "type": ItemType.PRODUCT,
            "reference": "FURN-001",
            "weight": 15.0,
            "categories": ["Furniture"]
        },
        {
            "name": "Fresh Produce Box",
            "type": ItemType.PRODUCT,
            "reference": "FOOD-001",
            "weight": 5.0,
            "temperature_min": 2.0,
            "temperature_max": 8.0,
            "categories": ["Food"]
        }
    ]
    
    product_ids = []
    for prod in products:
        # Create product
        item = client.create_delivery_item({
            "name": prod["name"],
            "item_type": prod["type"],
            "reference": prod["reference"],
            "weight": prod["weight"],
            "weight_unit": "kg",
            "is_fragile": prod.get("is_fragile", False),
            "temperature_min": prod.get("temperature_min"),
            "temperature_max": prod.get("temperature_max")
        })
        product_ids.append(str(item.id))
        print(f"✓ Imported: {item.name}")
        
        # Assign category tags
        category_tag_ids = [tag_ids[cat] for cat in prod["categories"] if cat in tag_ids]
        if category_tag_ids:
            client._request('POST', f'/catalog/delivery-items/{item.id}/assign_tags/', json={
                "object_ids": [str(item.id)],
                "tag_ids": category_tag_ids,
                "action": "add"
            })
    
    print(f"\n✓ Catalog organized with {len(product_ids)} products")
    return product_ids


def workflow_find_and_update():
    """
    Workflow for finding and updating resources.
    
    Demonstrates:
    - Searching for resources
    - Checking if resource exists
    - Updating multiple resources
    """
    print("\n=== Workflow: Find and Update ===\n")
    
    # Search for customers in specific city
    print("1. Finding all customers in Paris...")
    customers = client.list_customers(billing_city="Paris")
    print(f"   Found {customers.count} customers in Paris")
    
    # Update notes for all Paris customers
    if customers.count > 0:
        print("\n2. Updating Paris customers with location tag...")
        paris_customer_ids = [str(c.id) for c in customers.results]
        
        result = client.customer_bulk_action(
            action="append_notes",
            customer_ids=paris_customer_ids,
            notes=" - Located in Paris region"
        )
        print(f"✓ Updated {result.get('processed', 0)} customers")
    
    # Find fragile items and group them
    print("\n3. Finding all fragile items...")
    fragile_items = client.list_delivery_items(is_fragile=True)
    print(f"   Found {fragile_items.count} fragile items")
    
    if fragile_items.count > 0:
        # Create 'Handle with Care' tag if not exists
        try:
            tag = client.create_tag({
                "name": "Handle with Care",
                "color": "#FFA500"
            })
            print(f"✓ Created tag: {tag.name}")
            
            # Assign to all fragile items
            fragile_ids = [str(item.id) for item in fragile_items.results]
            client.delivery_item_bulk_action(
                action="add_tags",
                delivery_item_ids=fragile_ids,
                tags=[str(tag.id)]
            )
            print(f"✓ Tagged {len(fragile_ids)} fragile items")
            
        except Exception as e:
            print(f"Note: Tag might already exist or error occurred: {e}")


def workflow_check_resource_exists():
    """Demonstrate checking if resource exists before operations."""
    print("\n=== Workflow: Check Resource Exists ===\n")
    
    test_customer_id = "00000000-0000-0000-0000-000000000000"
    
    # Method 1: Try-except pattern
    print("1. Using try-except to check existence...")
    try:
        customer = client.get_customer(test_customer_id)
        print(f"✓ Customer exists: {customer.display_name}")
    except NotFoundError:
        print("✗ Customer does not exist")
    
    # Method 2: Search by external_id
    print("\n2. Searching by external_id...")
    external_id = "EXT-001"
    customers = client.list_customers(external_id=external_id)
    
    if customers.count > 0:
        print(f"✓ Found customer with external_id {external_id}")
        customer = customers.results[0]
    else:
        print(f"✗ No customer found with external_id {external_id}")
        # Create new customer
        customer = client.create_customer({
            "customer_type": CustomerType.COMPANY,
            "company_name": "New Customer",
            "external_id": external_id,
            "billing_city": "Paris"
        })
        print(f"✓ Created new customer: {customer.display_name}")


def workflow_cleanup_inactive():
    """
    Workflow for cleaning up inactive resources.
    
    WARNING: This is a destructive operation!
    """
    print("\n=== Workflow: Cleanup Inactive Resources ===\n")
    print("⚠️  This workflow demonstrates cleanup - use with caution!\n")
    
    # Find inactive customers
    inactive_customers = client.list_customers(is_active=False)
    print(f"Found {inactive_customers.count} inactive customers")
    
    if inactive_customers.count > 0:
        print("\nInactive customers:")
        for customer in inactive_customers.results[:5]:  # Show first 5
            print(f"  - {customer.display_name} (ID: {customer.id})")
        
        # Note: Actual deletion would be done carefully
        print("\n(Deletion skipped in demo - remove this check for actual cleanup)")
        # Uncomment to actually delete:
        # for customer in inactive_customers.results:
        #     client.delete_customer(customer.id)
        #     print(f"✓ Deleted: {customer.display_name}")


def workflow_reporting():
    """Generate reports using SDK data."""
    print("\n=== Workflow: Generate Reports ===\n")
    
    # Customer summary
    print("1. Customer Summary Report")
    all_customers = client.list_customers()
    active_customers = client.list_customers(is_active=True)
    company_customers = client.list_customers(customer_type=CustomerType.COMPANY)
    
    print(f"   Total customers: {all_customers.count}")
    print(f"   Active customers: {active_customers.count}")
    print(f"   Company customers: {company_customers.count}")
    print(f"   Individual customers: {all_customers.count - company_customers.count}")
    
    # Location summary
    print("\n2. Location Summary Report")
    all_locations = client.list_delivery_locations()
    with_gps = client.list_delivery_locations(has_coordinates=True)
    truck_accessible = client.list_delivery_locations(truck_access=True)
    
    print(f"   Total locations: {all_locations.count}")
    print(f"   With GPS coordinates: {with_gps.count}")
    print(f"   Truck accessible: {truck_accessible.count}")
    
    # Vehicle summary
    print("\n3. Vehicle Summary Report")
    vehicles = client.list_vehicles()
    available = client.list_vehicles(status="available")
    in_maintenance = client.list_vehicles(status="maintenance")
    
    print(f"   Total vehicles: {len(vehicles)}")
    print(f"   Available: {len(available)}")
    print(f"   In maintenance: {len(in_maintenance)}")
    
    # Product summary
    print("\n4. Product Catalog Report")
    all_items = client.list_delivery_items()
    products = client.list_delivery_items(item_type=ItemType.PRODUCT)
    fragile = client.list_delivery_items(is_fragile=True)
    
    print(f"   Total items: {all_items.count}")
    print(f"   Products: {products.count}")
    print(f"   Fragile items: {fragile.count}")


def workflow_data_migration():
    """
    Workflow for migrating data between environments.
    
    Use case: Copy data from test to production
    """
    print("\n=== Workflow: Data Migration ===\n")
    
    # Source client (e.g., test environment)
    source_client = MapFlowClient(
        api_key="test-api-key",
        base_url="https://api-test.mapflow.co"
    )
    
    # Destination client (e.g., production)
    dest_client = MapFlowClient(
        api_key="prod-api-key",
        base_url="https://api.mapflow.co"
    )
    
    print("Exporting tags from test environment...")
    source_tags = source_client.list_tags()
    
    print(f"Found {source_tags.count} tags to migrate")
    
    migrated_count = 0
    for tag in source_tags.results:
        try:
            # Check if tag already exists in destination
            dest_tags = dest_client.list_tags(name=tag.name)
            
            if dest_tags.count == 0:
                # Create in destination
                dest_client.create_tag({
                    "name": tag.name,
                    "color": tag.color,
                    "description": tag.description
                })
                print(f"✓ Migrated tag: {tag.name}")
                migrated_count += 1
            else:
                print(f"⊙ Tag already exists: {tag.name}")
                
        except Exception as e:
            print(f"✗ Error migrating tag {tag.name}: {e}")
    
    print(f"\n✓ Migration complete: {migrated_count} tags migrated")


def main():
    """Run workflow examples."""
    print("="*60)
    print("MapFlow SDK - Common Workflows")
    print("="*60)
    
    print("\nAvailable workflows:")
    print("1. Onboard New Customer (complete setup)")
    print("2. Setup Vehicle Fleet")
    print("3. Organize Product Catalog")
    print("4. Find and Update Resources")
    print("5. Check Resource Exists")
    print("6. Generate Reports")
    print("7. Cleanup Inactive Resources")
    print("8. Data Migration")
    
    choice = input("\nSelect workflow (1-8) or 'all' to run all: ").strip()
    
    try:
        if choice == "1" or choice == "all":
            workflow_onboard_new_customer()
        
        if choice == "2" or choice == "all":
            workflow_setup_fleet()
        
        if choice == "3" or choice == "all":
            workflow_organize_catalog()
        
        if choice == "4" or choice == "all":
            workflow_find_and_update()
        
        if choice == "5" or choice == "all":
            workflow_check_resource_exists()
        
        if choice == "6" or choice == "all":
            workflow_reporting()
        
        if choice == "7":
            workflow_cleanup_inactive()
        
        if choice == "8":
            print("\nNote: Data migration requires separate test/prod API keys")
            print("Skipping in demo mode")
        
        print("\n" + "="*60)
        print("Workflows completed!")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

