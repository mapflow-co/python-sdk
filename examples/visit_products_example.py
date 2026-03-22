"""
Visit Products Example - MapFlow SDK.

This example demonstrates how to work with visit products (products assigned to visits).

Note: This requires having visits created in your MapFlow account.
You can create visits via the web interface or the /visits/visits/ endpoint.
"""

from mapflow import (
    MapFlowClient,
    VisitProduct,
    VisitProductCreate,
    NotFoundError,
    ValidationError
)

# Initialize client
API_KEY = "your-api-key-here"
client = MapFlowClient(api_key=API_KEY)


def list_visit_products_example():
    """List all visit products with filtering."""
    print("\n=== Listing Visit Products ===\n")
    
    # List all visit products
    visit_products = client.list_visit_products()
    print(f"Total visit products: {visit_products.count}")
    
    # List with pagination
    page1 = client.list_visit_products(page=1, page_size=10)
    print(f"Page 1: {len(page1.results)} items")
    
    # Filter by visit
    # visit_products = client.list_visit_products(visit="visit-uuid-here")
    
    # Filter by product
    # visit_products = client.list_visit_products(product="product-uuid-here")
    
    # Filter by quantity range
    high_quantity = client.list_visit_products(min_quantity=10)
    print(f"Visit products with quantity >= 10: {high_quantity.count}")
    
    # Search globally
    search_results = client.list_visit_products(search="laptop")
    print(f"Search results for 'laptop': {search_results.count}")
    
    # Display details
    if visit_products.count > 0:
        print("\nFirst 3 visit products:")
        for i, vp in enumerate(visit_products.results[:3], 1):
            print(f"\n{i}. Visit Product ID: {vp.id}")
            print(f"   Quantity: {vp.quantity}")
            if vp.total_weight_kg:
                print(f"   Total weight: {vp.total_weight_kg} kg")
            if vp.total_volume_m3:
                print(f"   Total volume: {vp.total_volume_m3} m³")


def create_visit_product_example(visit_id, product_id):
    """Add a product to a visit."""
    print("\n=== Creating Visit Product ===\n")
    
    try:
        # Create visit product using dict
        visit_product = client.create_visit_product({
            "visit": visit_id,
            "product": product_id,
            "quantity": 5
        })
        
        print(f"✓ Product added to visit!")
        print(f"  ID: {visit_product.id}")
        print(f"  Visit: {visit_product.visit}")
        print(f"  Product: {visit_product.product}")
        print(f"  Quantity: {visit_product.quantity}")
        
        if visit_product.total_weight_kg:
            print(f"  Total weight: {visit_product.total_weight_kg} kg")
        if visit_product.total_volume_m3:
            print(f"  Total volume: {visit_product.total_volume_m3} m³")
        
        return visit_product.id
        
    except ValidationError as e:
        print(f"✗ Validation error: {e.message}")
        print(f"  Details: {e.response}")
        return None


def create_visit_product_with_model(visit_id, product_id):
    """Create visit product using Pydantic model."""
    print("\n=== Creating Visit Product with Pydantic Model ===\n")
    
    try:
        # Create using Pydantic model for validation
        visit_product_data = VisitProductCreate(
            visit=visit_id,
            product=product_id,
            quantity=10
        )
        
        # Pydantic validates quantity >= 0
        print(f"✓ Model validated: quantity = {visit_product_data.quantity}")
        
        # Create in API
        visit_product = client.create_visit_product(visit_product_data)
        
        print(f"✓ Visit product created: {visit_product.id}")
        return visit_product.id
        
    except ValidationError as e:
        print(f"✗ Validation error: {e.message}")
        return None


def update_visit_product_example(visit_product_id):
    """Update visit product quantity."""
    print("\n=== Updating Visit Product ===\n")
    
    try:
        # Get current visit product
        visit_product = client.get_visit_product(visit_product_id)
        print(f"Current quantity: {visit_product.quantity}")
        
        # Update quantity
        new_quantity = visit_product.quantity + 5
        updated = client.patch_visit_product(visit_product_id, {
            "quantity": new_quantity
        })
        
        print(f"✓ Quantity updated: {visit_product.quantity} → {updated.quantity}")
        
        return updated
        
    except NotFoundError:
        print("✗ Visit product not found")
        return None


def bulk_update_quantities(visit_product_ids, new_quantity):
    """Bulk update quantities for multiple visit products."""
    print("\n=== Bulk Update Quantities ===\n")
    
    try:
        # Update all to same quantity
        result = client.visit_product_bulk_action(
            action="update_quantity",
            visitproduct_ids=visit_product_ids,
            new_quantity=new_quantity
        )
        
        print(f"✓ Bulk action completed!")
        print(f"  Processed: {result.get('processed', 0)} items")
        
        if result.get('errors'):
            print(f"  Errors: {len(result['errors'])}")
            for error in result['errors'][:3]:
                print(f"    - {error}")
        
        return result
        
    except ValidationError as e:
        print(f"✗ Validation error: {e.message}")
        return None


def multiply_quantities(visit_product_ids, multiplier):
    """Multiply quantities for multiple visit products."""
    print("\n=== Multiply Quantities ===\n")
    
    try:
        # Multiply all quantities by a factor
        result = client.visit_product_bulk_action(
            action="multiply_quantity",
            visitproduct_ids=visit_product_ids,
            quantity_multiplier=str(multiplier)
        )
        
        print(f"✓ Quantities multiplied by {multiplier}!")
        print(f"  Processed: {result.get('processed', 0)} items")
        
        return result
        
    except ValidationError as e:
        print(f"✗ Validation error: {e.message}")
        return None


def advanced_filtering_example():
    """Demonstrate advanced filtering capabilities."""
    print("\n=== Advanced Filtering ===\n")
    
    # Filter by weight range
    heavy_products = client.list_visit_products(
        min_total_weight=10.0,
        max_total_weight=100.0
    )
    print(f"Visit products with 10-100kg total weight: {heavy_products.count}")
    
    # Filter by volume range
    large_volume = client.list_visit_products(
        min_total_volume=0.5,
        max_total_volume=5.0
    )
    print(f"Visit products with 0.5-5.0m³ total volume: {large_volume.count}")
    
    # Filter by customer
    # customer_products = client.list_visit_products(customer="customer-uuid")
    
    # Filter by location
    # location_products = client.list_visit_products(location="location-uuid")
    
    # Filter by customer city
    paris_products = client.list_visit_products(location_city="Paris")
    print(f"Visit products for Paris locations: {paris_products.count}")
    
    # Combined filters
    filtered = client.list_visit_products(
        min_quantity=5,
        has_weight=True,
        has_volume=True
    )
    print(f"Visit products (qty>=5, with weight & volume): {filtered.count}")


def report_visit_products():
    """Generate a report of visit products."""
    print("\n=== Visit Products Report ===\n")
    
    # Get all visit products
    all_vps = client.list_visit_products()
    
    if all_vps.count == 0:
        print("No visit products found.")
        return
    
    print(f"Total visit products: {all_vps.count}")
    
    # Statistics
    total_quantity = 0
    total_weight = 0.0
    total_volume = 0.0
    
    page = 1
    while True:
        response = client.list_visit_products(page=page)
        
        for vp in response.results:
            total_quantity += vp.quantity
            if vp.total_weight_kg:
                total_weight += float(vp.total_weight_kg)
            if vp.total_volume_m3:
                total_volume += float(vp.total_volume_m3)
        
        if not response.next:
            break
        page += 1
    
    print(f"\nAggregate Statistics:")
    print(f"  Total quantity across all visit products: {total_quantity}")
    print(f"  Total weight: {total_weight:.2f} kg")
    print(f"  Total volume: {total_volume:.4f} m³")


def main():
    """Run visit products examples."""
    print("="*80)
    print("MapFlow SDK - Visit Products Examples")
    print("="*80)
    
    print("\nNote: Visit products link products to visits.")
    print("You need to have visits created in your MapFlow account to test fully.")
    
    # List existing visit products
    list_visit_products_example()
    
    # Advanced filtering
    advanced_filtering_example()
    
    # Generate report
    report_visit_products()
    
    # Interactive creation (requires visit_id and product_id)
    print("\n" + "-"*80)
    create_new = input("\nDo you want to create a new visit product? (y/n): ").strip().lower()
    
    if create_new == 'y':
        visit_id = input("Enter visit UUID: ").strip()
        product_id = input("Enter product UUID: ").strip()
        quantity = int(input("Enter quantity: ").strip() or "1")
        
        try:
            visit_product = client.create_visit_product({
                "visit": visit_id,
                "product": product_id,
                "quantity": quantity
            })
            
            print(f"\n✓ Visit product created: {visit_product.id}")
            
            # Ask if want to delete
            delete = input("\nDelete this visit product? (y/n): ").strip().lower()
            if delete == 'y':
                client.delete_visit_product(visit_product.id)
                print("✓ Visit product deleted")
                
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    print("\n" + "="*80)
    print("Examples completed!")
    print("="*80)


if __name__ == "__main__":
    main()


