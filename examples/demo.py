#!/usr/bin/env python3
"""
Demo script for MapFlow SDK.

This script demonstrates how to use the SDK with your API key.
Set your API key as an environment variable or replace the placeholder below.
"""

import os
import sys
from pprint import pprint

from mapflow import (
    MapFlowClient,
    CustomerType,
    ItemType,
    VehicleType,
    WarehouseType,
    MapFlowError,
    AuthenticationError,
    NotFoundError
)


def get_api_key():
    """Get API key from environment or user input."""
    api_key = os.getenv('MAPFLOW_API_KEY')
    
    if not api_key:
        print("No API key found in environment variable MAPFLOW_API_KEY")
        api_key = input("Enter your MapFlow API key: ").strip()
        
        if not api_key:
            print("Error: API key is required")
            sys.exit(1)
    
    return api_key


def demo_basic_operations(client):
    """Demonstrate basic CRUD operations."""
    print("\n" + "="*60)
    print("DEMO: Basic Operations")
    print("="*60)
    
    try:
        # List existing customers
        print("\n1. Listing existing customers...")
        customers = client.list_customers(page=1)
        print(f"   Total customers: {customers.count}")
        
        if customers.results:
            print(f"   First customer: {customers.results[0]}")
        
        # List delivery locations
        print("\n2. Listing delivery locations...")
        locations = client.list_delivery_locations(page=1)
        print(f"   Total locations: {locations.count}")
        
        # List warehouses
        print("\n3. Listing warehouses...")
        warehouses = client.list_warehouses(page=1)
        print(f"   Total warehouses: {warehouses.count}")
        
        # List delivery items
        print("\n4. Listing delivery items...")
        items = client.list_delivery_items(page=1)
        print(f"   Total items: {items.count}")
        
        # List vehicles
        print("\n5. Listing vehicles...")
        vehicles = client.list_vehicles()
        print(f"   Total vehicles: {len(vehicles)}")
        
        # List tags
        print("\n6. Listing tags...")
        tags = client.list_tags(page=1)
        print(f"   Total tags: {tags.count}")
        
    except AuthenticationError:
        print("\n✗ Authentication failed. Please check your API key.")
        sys.exit(1)
    except MapFlowError as e:
        print(f"\n✗ API Error: {e.message}")
        sys.exit(1)


def demo_search_and_filter(client):
    """Demonstrate search and filtering capabilities."""
    print("\n" + "="*60)
    print("DEMO: Search and Filtering")
    print("="*60)
    
    try:
        # Search customers
        print("\n1. Searching customers (is_active=True)...")
        active_customers = client.list_customers(is_active=True)
        print(f"   Active customers: {active_customers.count}")
        
        # Filter locations by city
        print("\n2. Filtering locations by city='Paris'...")
        paris_locations = client.list_delivery_locations(city="Paris")
        print(f"   Locations in Paris: {paris_locations.count}")
        
        # Filter items by type
        print("\n3. Filtering items by type=PRODUCT...")
        products = client.list_delivery_items(item_type=ItemType.PRODUCT)
        print(f"   Products: {products.count}")
        
        # Filter vehicles by status
        print("\n4. Filtering vehicles by status=available...")
        available_vehicles = client.list_vehicles(status="available")
        print(f"   Available vehicles: {len(available_vehicles)}")
        
    except MapFlowError as e:
        print(f"\n✗ Error: {e.message}")


def demo_statistics(client):
    """Demonstrate statistics endpoints."""
    print("\n" + "="*60)
    print("DEMO: Statistics")
    print("="*60)
    
    try:
        # Customer stats
        print("\n1. Getting delivery items statistics...")
        stats = client._request('GET', '/catalog/delivery-items/stats/')
        print("   Stats retrieved:")
        pprint(stats)
        
        # Driver/Picker stats
        print("\n2. Getting drivers/pickers statistics...")
        driver_stats = client._request('GET', '/drivers-pickers/people/stats/')
        print("   Stats retrieved:")
        pprint(driver_stats)
        
    except MapFlowError as e:
        print(f"\n✗ Error: {e.message}")


def demo_get_details(client):
    """Demonstrate getting detailed information."""
    print("\n" + "="*60)
    print("DEMO: Getting Detailed Information")
    print("="*60)
    
    try:
        # Get first customer with details
        customers = client.list_customers(page=1)
        
        if customers.results and len(customers.results) > 0:
            first_customer_id = customers.results[0].id
            
            print(f"\n1. Getting details for customer {first_customer_id}...")
            customer = client.get_customer(first_customer_id)
            print(f"   Display name: {customer.display_name}")
            print(f"   Type: {customer.customer_type}")
            print(f"   Active: {customer.is_active}")
            
            # Get customer locations
            print("\n2. Getting customer locations...")
            locations = client.get_customer_locations(first_customer_id)
            print(f"   Total locations: {len(locations)}")
            
            for i, loc in enumerate(locations[:3], 1):
                print(f"   Location {i}: {loc.name} - {loc.city}")
        else:
            print("\n   No customers found in your organization.")
        
    except NotFoundError:
        print("\n   Customer not found")
    except MapFlowError as e:
        print(f"\n✗ Error: {e.message}")


def interactive_menu(client):
    """Interactive menu for testing different operations."""
    while True:
        print("\n" + "="*60)
        print("MapFlow SDK Demo - Interactive Menu")
        print("="*60)
        print("\n1. Basic Operations (list resources)")
        print("2. Search and Filter")
        print("3. Statistics")
        print("4. Get Details")
        print("5. Run All Demos")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            demo_basic_operations(client)
        elif choice == "2":
            demo_search_and_filter(client)
        elif choice == "3":
            demo_statistics(client)
        elif choice == "4":
            demo_get_details(client)
        elif choice == "5":
            demo_basic_operations(client)
            demo_search_and_filter(client)
            demo_statistics(client)
            demo_get_details(client)
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")


def main():
    """Main demo function."""
    print("="*60)
    print("MapFlow Python SDK - Demo")
    print("="*60)
    
    # Get API key
    api_key = get_api_key()
    
    # Get base URL (optional)
    base_url = os.getenv('MAPFLOW_BASE_URL', 'https://api.mapflow.co')
    
    # Initialize client
    print(f"\nInitializing client...")
    print(f"Base URL: {base_url}")
    
    client = MapFlowClient(
        api_key=api_key,
        base_url=base_url
    )
    
    print("✓ Client initialized successfully!")
    
    # Check if running in interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        # Run all demos automatically
        demo_basic_operations(client)
        demo_search_and_filter(client)
        demo_statistics(client)
        demo_get_details(client)
    else:
        # Interactive menu
        interactive_menu(client)


if __name__ == "__main__":
    main()

