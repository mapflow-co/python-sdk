"""
Integration example - Real-world scenario.

This example demonstrates a complete integration scenario:
1. Import customer data from external system
2. Create delivery locations
3. Add products to catalog
4. Set up warehouses and vehicles
5. Create tags for organization
"""

import json
from mapflow import (
    MapFlowClient,
    CustomerType,
    ItemType,
    VehicleType,
    WarehouseType,
    NotFoundError,
    ValidationError
)


# Initialize client
API_KEY = "your-api-key-here"
client = MapFlowClient(api_key=API_KEY)


def import_customer_data(customer_data_list):
    """
    Import customers from external system.
    
    Args:
        customer_data_list: List of customer dictionaries from external system
    
    Returns:
        Dictionary mapping external IDs to MapFlow customer IDs
    """
    print("\n=== Importing Customer Data ===\n")
    
    customer_mapping = {}
    
    for ext_customer in customer_data_list:
        try:
            # Create customer with external reference
            customer = client.create_customer({
                "customer_type": ext_customer.get("type", CustomerType.COMPANY),
                "company_name": ext_customer.get("company_name"),
                "first_name": ext_customer.get("first_name"),
                "last_name": ext_customer.get("last_name"),
                "email": ext_customer.get("email"),
                "phone": ext_customer.get("phone"),
                "billing_address": ext_customer.get("address"),
                "billing_zip_code": ext_customer.get("zip_code"),
                "billing_city": ext_customer.get("city"),
                "billing_country": ext_customer.get("country", "FR"),
                "external_id": ext_customer.get("external_id"),
                "external_reference": ext_customer.get("external_ref"),
                "siret": ext_customer.get("siret"),
                "is_active": True
            })
            
            customer_mapping[ext_customer["external_id"]] = str(customer.id)
            print(f"✓ Imported: {customer.display_name} (External ID: {ext_customer['external_id']})")
            
        except ValidationError as e:
            print(f"✗ Validation error for {ext_customer.get('company_name')}: {e.message}")
        except Exception as e:
            print(f"✗ Error importing customer: {e}")
    
    print(f"\nImported {len(customer_mapping)} customers successfully")
    return customer_mapping


def create_delivery_locations(customer_mapping, location_data_list):
    """
    Create delivery locations for imported customers.
    
    Args:
        customer_mapping: Dictionary mapping external customer IDs to MapFlow IDs
        location_data_list: List of location dictionaries
    
    Returns:
        List of created delivery location IDs
    """
    print("\n=== Creating Delivery Locations ===\n")
    
    location_ids = []
    
    for loc_data in location_data_list:
        try:
            # Get MapFlow customer ID from external customer ID
            customer_id = customer_mapping.get(loc_data["customer_external_id"])
            
            if not customer_id:
                print(f"✗ Customer not found for external ID: {loc_data['customer_external_id']}")
                continue
            
            location = client.create_delivery_location({
                "customer": customer_id,
                "name": loc_data["name"],
                "address": loc_data["address"],
                "zip_code": loc_data["zip_code"],
                "city": loc_data["city"],
                "country": loc_data.get("country", "FR"),
                "latitude": loc_data.get("latitude"),
                "longitude": loc_data.get("longitude"),
                "truck_access": loc_data.get("truck_access", False),
                "loading_dock": loc_data.get("loading_dock", False),
                "delivery_instructions": loc_data.get("delivery_instructions"),
                "is_active": True
            })
            
            location_ids.append(str(location.id))
            print(f"✓ Created: {location.name} for {location.customer_display_name}")
            
        except Exception as e:
            print(f"✗ Error creating location: {e}")
    
    print(f"\nCreated {len(location_ids)} delivery locations")
    return location_ids


def setup_warehouses(warehouse_data_list):
    """
    Set up warehouses for route optimization.
    
    Args:
        warehouse_data_list: List of warehouse dictionaries
    
    Returns:
        List of created warehouse IDs
    """
    print("\n=== Setting Up Warehouses ===\n")
    
    warehouse_ids = []
    
    for wh_data in warehouse_data_list:
        try:
            warehouse = client.create_warehouse({
                "name": wh_data["name"],
                "code": wh_data["code"],
                "warehouse_type": wh_data.get("type", WarehouseType.HUB),
                "address": wh_data["address"],
                "zip_code": wh_data["zip_code"],
                "city": wh_data["city"],
                "country": wh_data.get("country", "FR"),
                "latitude": wh_data.get("latitude"),
                "longitude": wh_data.get("longitude"),
                "opening_time": wh_data.get("opening_time", "08:00:00"),
                "closing_time": wh_data.get("closing_time", "18:00:00"),
                "is_start_point": wh_data.get("is_start_point", True),
                "is_end_point": wh_data.get("is_end_point", True),
                "has_loading_dock": wh_data.get("has_loading_dock", True),
                "max_vehicles": wh_data.get("max_vehicles", 50),
                "is_default": wh_data.get("is_default", False)
            })
            
            warehouse_ids.append(str(warehouse.id))
            print(f"✓ Created: {warehouse.name} ({warehouse.code})")
            
            # Set first warehouse as default
            if wh_data.get("is_default", False):
                client.set_default_warehouse(warehouse.id)
                print(f"  → Set as default warehouse")
            
        except Exception as e:
            print(f"✗ Error creating warehouse: {e}")
    
    print(f"\nCreated {len(warehouse_ids)} warehouses")
    return warehouse_ids


def import_product_catalog(product_data_list):
    """
    Import products into catalog.
    
    Args:
        product_data_list: List of product dictionaries
    
    Returns:
        List of created product IDs
    """
    print("\n=== Importing Product Catalog ===\n")
    
    product_ids = []
    
    for prod_data in product_data_list:
        try:
            item = client.create_delivery_item({
                "name": prod_data["name"],
                "item_type": prod_data.get("type", ItemType.PRODUCT),
                "reference": prod_data.get("reference"),
                "barcode": prod_data.get("barcode"),
                "weight": prod_data.get("weight"),
                "weight_unit": prod_data.get("weight_unit", "kg"),
                "length": prod_data.get("length"),
                "width": prod_data.get("width"),
                "height": prod_data.get("height"),
                "is_fragile": prod_data.get("is_fragile", False),
                "is_dangerous": prod_data.get("is_dangerous", False),
                "declared_value": prod_data.get("value"),
                "currency": prod_data.get("currency", "EUR"),
                "buying_price": prod_data.get("cost"),
                "selling_price": prod_data.get("price"),
                "vat_rate": prod_data.get("vat", 20.0)
            })
            
            product_ids.append(str(item.id))
            print(f"✓ Imported: {item.name} (Ref: {item.reference})")
            
        except Exception as e:
            print(f"✗ Error importing product {prod_data.get('name')}: {e}")
    
    print(f"\nImported {len(product_ids)} products")
    return product_ids


def create_fleet(vehicle_data_list, warehouse_ids):
    """
    Create vehicle fleet.
    
    Args:
        vehicle_data_list: List of vehicle dictionaries
        warehouse_ids: List of warehouse IDs to assign vehicles to
    
    Returns:
        List of created vehicle IDs
    """
    print("\n=== Creating Vehicle Fleet ===\n")
    
    vehicle_ids = []
    
    for veh_data in vehicle_data_list:
        try:
            vehicle = client.create_vehicle({
                "name": veh_data["name"],
                "license_plate": veh_data["license_plate"],
                "vehicle_type": veh_data.get("type", VehicleType.VAN_MEDIUM),
                "brand": veh_data.get("brand"),
                "model": veh_data.get("model"),
                "year": veh_data.get("year"),
                "energy_type": veh_data.get("energy_type"),
                "max_weight_kg": veh_data.get("max_weight"),
                "max_volume_m3": veh_data.get("max_volume"),
                "max_distance_km": veh_data.get("max_distance"),
                "status": "available",
                "assigned_warehouses": warehouse_ids[:1] if warehouse_ids else []
            })
            
            vehicle_ids.append(str(vehicle.id))
            print(f"✓ Created: {vehicle.name} ({vehicle.license_plate})")
            
        except Exception as e:
            print(f"✗ Error creating vehicle: {e}")
    
    print(f"\nCreated {len(vehicle_ids)} vehicles")
    return vehicle_ids


def setup_tags():
    """
    Create organizational tags.
    
    Returns:
        Dictionary of tag names to IDs
    """
    print("\n=== Setting Up Tags ===\n")
    
    tags_to_create = [
        {"name": "Urgent", "color": "#FF0000", "description": "Urgent deliveries"},
        {"name": "Fragile", "color": "#FFA500", "description": "Fragile items"},
        {"name": "VIP", "color": "#FFD700", "description": "VIP customers"},
        {"name": "Express", "color": "#00FF00", "description": "Express delivery"},
        {"name": "Standard", "color": "#0000FF", "description": "Standard delivery"}
    ]
    
    tag_mapping = {}
    
    for tag_data in tags_to_create:
        try:
            tag = client.create_tag(tag_data)
            tag_mapping[tag.name] = str(tag.id)
            print(f"✓ Created tag: {tag.name} ({tag.color})")
        except Exception as e:
            print(f"✗ Error creating tag {tag_data['name']}: {e}")
    
    print(f"\nCreated {len(tag_mapping)} tags")
    return tag_mapping


def main():
    """Run complete integration example."""
    print("=" * 60)
    print("MapFlow Integration Example")
    print("=" * 60)
    
    # Sample data (would normally come from external system/database)
    
    customers_data = [
        {
            "external_id": "EXT-001",
            "external_ref": "CLIENT-2024-001",
            "type": CustomerType.COMPANY,
            "company_name": "Tech Solutions SARL",
            "email": "contact@techsolutions.fr",
            "phone": "+33123456789",
            "address": "10 rue Innovation",
            "zip_code": "69001",
            "city": "Lyon",
            "country": "FR",
            "siret": "12345678901234"
        },
        {
            "external_id": "EXT-002",
            "external_ref": "CLIENT-2024-002",
            "type": CustomerType.COMPANY,
            "company_name": "Logistique Pro",
            "email": "contact@logistiquepro.fr",
            "phone": "+33987654321",
            "address": "25 avenue Commerce",
            "zip_code": "75008",
            "city": "Paris",
            "country": "FR",
            "siret": "98765432109876"
        }
    ]
    
    locations_data = [
        {
            "customer_external_id": "EXT-001",
            "name": "Entrepôt Lyon Sud",
            "address": "50 boulevard Industriel",
            "zip_code": "69200",
            "city": "Vénissieux",
            "latitude": 45.6975,
            "longitude": 4.8872,
            "truck_access": True,
            "loading_dock": True,
            "delivery_instructions": "Livraison quai 5"
        },
        {
            "customer_external_id": "EXT-002",
            "name": "Bureau Paris Centre",
            "address": "15 rue Opéra",
            "zip_code": "75009",
            "city": "Paris",
            "latitude": 48.8719,
            "longitude": 2.3314,
            "truck_access": False,
            "loading_dock": False
        }
    ]
    
    warehouses_data = [
        {
            "name": "Hub Principal Paris",
            "code": "HUB-PARIS",
            "type": WarehouseType.HUB,
            "address": "100 rue Logistique",
            "zip_code": "93200",
            "city": "Saint-Denis",
            "latitude": 48.9356,
            "longitude": 2.3539,
            "is_default": True,
            "has_loading_dock": True,
            "max_vehicles": 100
        }
    ]
    
    products_data = [
        {
            "name": "Ordinateur Portable Standard",
            "reference": "LAPTOP-001",
            "type": ItemType.PRODUCT,
            "barcode": "3760123456789",
            "weight": 2.5,
            "length": 35,
            "width": 25,
            "height": 3,
            "is_fragile": True,
            "value": 800.0,
            "cost": 500.0,
            "price": 800.0,
            "vat": 20.0
        },
        {
            "name": "Écran LED 24 pouces",
            "reference": "SCREEN-001",
            "type": ItemType.PRODUCT,
            "weight": 4.0,
            "is_fragile": True,
            "value": 300.0,
            "cost": 180.0,
            "price": 300.0
        }
    ]
    
    vehicles_data = [
        {
            "name": "Fourgon Livraison 01",
            "license_plate": "AB-123-CD",
            "type": VehicleType.VAN_MEDIUM,
            "brand": "Renault",
            "model": "Master",
            "year": 2023,
            "energy_type": "diesel",
            "max_weight": 1500,
            "max_volume": 12.0,
            "max_distance": 500
        },
        {
            "name": "Fourgon Livraison 02",
            "license_plate": "EF-456-GH",
            "type": VehicleType.VAN_MEDIUM,
            "brand": "Mercedes",
            "model": "Sprinter",
            "year": 2023,
            "energy_type": "electric",
            "max_weight": 1200,
            "max_volume": 10.0,
            "max_distance": 250
        }
    ]
    
    try:
        # Step 1: Import customers
        customer_mapping = import_customer_data(customers_data)
        
        # Step 2: Create delivery locations
        location_ids = create_delivery_locations(customer_mapping, locations_data)
        
        # Step 3: Set up warehouses
        warehouse_ids = setup_warehouses(warehouses_data)
        
        # Step 4: Import product catalog
        product_ids = import_product_catalog(products_data)
        
        # Step 5: Create vehicle fleet
        vehicle_ids = create_fleet(vehicles_data, warehouse_ids)
        
        # Step 6: Set up tags
        tag_mapping = setup_tags()
        
        # Summary
        print("\n" + "=" * 60)
        print("Integration Summary")
        print("=" * 60)
        print(f"Customers imported: {len(customer_mapping)}")
        print(f"Locations created: {len(location_ids)}")
        print(f"Warehouses set up: {len(warehouse_ids)}")
        print(f"Products imported: {len(product_ids)}")
        print(f"Vehicles created: {len(vehicle_ids)}")
        print(f"Tags created: {len(tag_mapping)}")
        print("\n✓ Integration completed successfully!\n")
        
        # Optional: Tag some customers as VIP
        if customer_mapping and "VIP" in tag_mapping:
            print("Tagging first customer as VIP...")
            first_customer_id = list(customer_mapping.values())[0]
            client.customer_bulk_action(
                action="add_tags",
                customer_ids=[first_customer_id],
                tag_ids=[tag_mapping["VIP"]]
            )
            print("✓ Tagged customer as VIP")
        
    except Exception as e:
        print(f"\n✗ Integration failed: {e}")
        import traceback
        traceback.print_exc()


def export_data_example():
    """Example of exporting data from MapFlow."""
    print("\n=== Exporting Data Example ===\n")
    
    # Get all active customers with their locations
    customers = client.list_customers(is_active=True)
    
    export_data = []
    
    for customer_data in customers.results:
        # Get full customer details
        customer = client.get_customer(customer_data.id)
        
        # Get customer locations
        locations = client.get_customer_locations(customer.id)
        
        export_record = {
            "customer_id": str(customer.id),
            "display_name": customer.display_name,
            "customer_type": customer.customer_type,
            "email": customer.email,
            "phone": customer.phone,
            "total_locations": len(locations),
            "locations": [
                {
                    "name": loc.name,
                    "address": loc.address,
                    "city": loc.city,
                    "has_gps": loc.has_coordinates
                }
                for loc in locations
            ]
        }
        
        export_data.append(export_record)
    
    # Save to JSON file
    with open('customer_export.json', 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Exported {len(export_data)} customers to customer_export.json")


def sync_example():
    """Example of syncing external system with MapFlow."""
    print("\n=== Sync Example ===\n")
    
    # External system data (example)
    external_customers = {
        "EXT-001": {"name": "Updated Company Name", "email": "newemail@company.com"},
        "EXT-002": {"name": "Another Update", "is_active": False}
    }
    
    # Get all customers from MapFlow
    customers = client.list_customers()
    
    updates_count = 0
    
    for customer_data in customers.results:
        customer = client.get_customer(customer_data.id)
        
        if customer.external_id in external_customers:
            external_data = external_customers[customer.external_id]
            
            # Update if data has changed
            update_payload = {}
            
            if external_data.get("name") and external_data["name"] != customer.company_name:
                update_payload["company_name"] = external_data["name"]
            
            if "email" in external_data and external_data["email"] != customer.email:
                update_payload["email"] = external_data["email"]
            
            if "is_active" in external_data and external_data["is_active"] != customer.is_active:
                update_payload["is_active"] = external_data["is_active"]
            
            if update_payload:
                client.patch_customer(customer.id, update_payload)
                print(f"✓ Updated: {customer.display_name}")
                updates_count += 1
    
    print(f"\n✓ Synced {updates_count} customers")


if __name__ == "__main__":
    # Run main integration
    main()
    
    # Uncomment to run additional examples:
    # export_data_example()
    # sync_example()

