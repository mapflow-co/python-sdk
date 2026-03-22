#!/usr/bin/env python3
"""
Getting Started with MapFlow SDK.

This interactive script helps you get started with the MapFlow SDK.
It will guide you through:
1. Setting up your API key
2. Testing the connection
3. Creating your first resources
"""

import os
import sys

from mapflow import (
    MapFlowClient,
    CustomerType,
    WarehouseType,
    ItemType,
    AuthenticationError,
    MapFlowError
)


def setup_api_key():
    """Help user set up API key."""
    print("\n" + "="*60)
    print("Step 1: API Key Setup")
    print("="*60)
    
    print("\nTo use the MapFlow SDK, you need an API key.")
    print("You can get one from: https://app.mapflow.co/settings/api-keys")
    
    # Check environment variable
    api_key = os.getenv('MAPFLOW_API_KEY')
    
    if api_key:
        print(f"\n✓ Found API key in environment variable MAPFLOW_API_KEY")
        use_env = input("Use this key? (y/n): ").strip().lower()
        if use_env != 'y':
            api_key = None
    
    if not api_key:
        print("\nEnter your MapFlow API key:")
        api_key = input("> ").strip()
        
        if not api_key:
            print("\n✗ API key is required. Exiting.")
            sys.exit(1)
        
        # Ask if they want to save it
        save = input("\nSave to environment variable? (y/n): ").strip().lower()
        if save == 'y':
            print("\nAdd this to your ~/.bashrc or ~/.zshrc:")
            print(f'export MAPFLOW_API_KEY="{api_key}"')
    
    return api_key


def test_connection(client):
    """Test API connection."""
    print("\n" + "="*60)
    print("Step 2: Testing Connection")
    print("="*60)
    
    try:
        # Try to list customers (simplest read operation)
        customers = client.list_customers(page=1)
        
        print("\n✓ Connection successful!")
        print(f"   Your organization has {customers.count} customer(s)")
        
        # Show some stats
        warehouses = client.list_warehouses(page=1)
        print(f"   Warehouses: {warehouses.count}")
        
        items = client.list_delivery_items(page=1)
        print(f"   Catalog items: {items.count}")
        
        vehicles = client.list_vehicles()
        print(f"   Vehicles: {len(vehicles)}")
        
        return True
        
    except AuthenticationError:
        print("\n✗ Authentication failed!")
        print("   Please check your API key and try again.")
        return False
    except MapFlowError as e:
        print(f"\n✗ Connection error: {e.message}")
        return False


def interactive_first_steps(client):
    """Interactive first steps guide."""
    print("\n" + "="*60)
    print("Step 3: Create Your First Resources")
    print("="*60)
    
    print("\nWhat would you like to create first?")
    print("1. Customer")
    print("2. Warehouse")
    print("3. Product")
    print("4. All of the above (recommended)")
    print("0. Skip")
    
    choice = input("\nEnter your choice: ").strip()
    
    created_ids = {}
    
    try:
        if choice in ["1", "4"]:
            # Create customer
            print("\n--- Creating Customer ---")
            print("Let's create a customer. Is it a company or individual?")
            print("1. Company")
            print("2. Individual")
            cust_type = input("Choice: ").strip()
            
            if cust_type == "1":
                company_name = input("Company name: ").strip() or "Demo Company"
                email = input("Email: ").strip() or "demo@example.com"
                city = input("City: ").strip() or "Paris"
                
                customer = client.create_customer({
                    "customer_type": CustomerType.COMPANY,
                    "company_name": company_name,
                    "email": email,
                    "billing_city": city,
                    "billing_country": "FR"
                })
            else:
                first_name = input("First name: ").strip() or "John"
                last_name = input("Last name: ").strip() or "Doe"
                email = input("Email: ").strip() or "john@example.com"
                
                customer = client.create_customer({
                    "customer_type": CustomerType.INDIVIDUAL,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "billing_city": "Paris",
                    "billing_country": "FR"
                })
            
            print(f"\n✓ Customer created: {customer.display_name}")
            print(f"   ID: {customer.id}")
            created_ids['customer'] = customer.id
        
        if choice in ["2", "4"]:
            # Create warehouse
            print("\n--- Creating Warehouse ---")
            name = input("Warehouse name (or press Enter for 'Main Hub'): ").strip() or "Main Hub"
            city = input("City (or press Enter for 'Paris'): ").strip() or "Paris"
            
            warehouse = client.create_warehouse({
                "name": name,
                "code": "HUB-01",
                "warehouse_type": WarehouseType.HUB,
                "address": "123 Logistics Blvd",
                "zip_code": "75001",
                "city": city,
                "country": "FR",
                "is_start_point": True,
                "is_end_point": True,
                "is_default": True
            })
            
            print(f"\n✓ Warehouse created: {warehouse.name}")
            print(f"   ID: {warehouse.id}")
            created_ids['warehouse'] = warehouse.id
        
        if choice in ["3", "4"]:
            # Create product
            print("\n--- Creating Product ---")
            name = input("Product name (or press Enter for 'Demo Product'): ").strip() or "Demo Product"
            weight = input("Weight in kg (or press Enter for '1.0'): ").strip() or "1.0"
            
            item = client.create_delivery_item({
                "name": name,
                "item_type": ItemType.PRODUCT,
                "reference": "DEMO-001",
                "weight": float(weight),
                "weight_unit": "kg",
                "currency": "EUR"
            })
            
            print(f"\n✓ Product created: {item.name}")
            print(f"   ID: {item.id}")
            created_ids['item'] = item.id
        
        if created_ids:
            print("\n" + "="*60)
            print("Summary of Created Resources")
            print("="*60)
            for resource_type, resource_id in created_ids.items():
                print(f"{resource_type.capitalize()}: {resource_id}")
            
            print("\n✓ You're all set! Start building your route optimization solution.")
        
    except MapFlowError as e:
        print(f"\n✗ Error creating resource: {e.message}")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")


def show_next_steps():
    """Show next steps to user."""
    print("\n" + "="*60)
    print("Next Steps")
    print("="*60)
    
    print("""
Now that you're set up, here are some things to try:

1. Explore the examples:
   - examples/basic_usage.py - Basic CRUD operations
   - examples/advanced_usage.py - Advanced features
   - examples/integration_example.py - Real-world integration
   - examples/common_workflows.py - Common use cases

2. Read the documentation:
   - README.md - Full documentation
   - API_REFERENCE.md - Complete API reference
   - QUICKSTART.md - Quick start guide

3. Build your integration:
   - Import your existing customer data
   - Set up your warehouse locations
   - Add your product catalog
   - Configure your vehicle fleet

4. Get help:
   - Documentation: https://mapflow.readme.io/reference
   - Support: support@mapflow.co
   - Examples: examples/ directory

Happy coding! 🚀
""")


def main():
    """Main getting started flow."""
    print("="*60)
    print("Welcome to MapFlow SDK!")
    print("="*60)
    print("\nThis script will help you get started with the MapFlow Python SDK.")
    
    # Step 1: Setup API key
    api_key = setup_api_key()
    
    # Initialize client
    print("\n✓ Initializing MapFlow client...")
    client = MapFlowClient(api_key=api_key)
    
    # Step 2: Test connection
    if not test_connection(client):
        print("\nPlease check your API key and try again.")
        sys.exit(1)
    
    # Step 3: Interactive first steps
    proceed = input("\nWould you like to create some resources? (y/n): ").strip().lower()
    if proceed == 'y':
        interactive_first_steps(client)
    
    # Show next steps
    show_next_steps()


if __name__ == "__main__":
    main()

