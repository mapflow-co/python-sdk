# Quick Start Guide - MapFlow Python SDK

Get started with the MapFlow Python SDK in 5 minutes!

## Installation

```bash
pip install mapflow-co-sdk
```

## Get Your API Key

1. Sign up at [mapflow.co](https://mapflow.co)
2. Navigate to Settings > API Keys
3. Create a new API key
4. Copy your key (keep it secure!)

## First Steps

### 1. Initialize the Client

```python
from mapflow import MapFlowClient

client = MapFlowClient(api_key="your-api-key")
```

### 2. Create Your First Customer

```python
from mapflow import CustomerType

# Create a company customer
customer = client.create_customer({
    "customer_type": CustomerType.COMPANY,
    "company_name": "My First Company",
    "email": "contact@company.com",
    "billing_city": "Paris",
    "billing_country": "FR"
})

print(f"Created customer: {customer.display_name}")
print(f"Customer ID: {customer.id}")
```

### 3. Add a Delivery Location

```python
location = client.create_delivery_location({
    "customer": customer.id,
    "name": "Main Office",
    "address": "123 Main Street",
    "zip_code": "75001",
    "city": "Paris",
    "country": "FR",
    "latitude": 48.8566,
    "longitude": 2.3522
})

print(f"Created location: {location.name}")
```

### 4. Create a Warehouse

```python
from mapflow import WarehouseType

warehouse = client.create_warehouse({
    "name": "Central Warehouse",
    "code": "MAIN-01",
    "warehouse_type": WarehouseType.HUB,
    "address": "456 Warehouse Blvd",
    "zip_code": "93200",
    "city": "Saint-Denis",
    "country": "FR",
    "is_start_point": True,
    "is_end_point": True
})

print(f"Created warehouse: {warehouse.name}")
```

### 5. Add Products to Catalog

```python
from mapflow import ItemType

product = client.create_delivery_item({
    "name": "Laptop Computer",
    "item_type": ItemType.PRODUCT,
    "weight": 2.5,
    "weight_unit": "kg",
    "declared_value": 1000.0,
    "currency": "EUR",
    "is_fragile": True
})

print(f"Created product: {product.name}")
```

### 6. Create a Vehicle

```python
from mapflow import VehicleType, EnergyType

vehicle = client.create_vehicle({
    "name": "Delivery Van 01",
    "license_plate": "AB-123-CD",
    "vehicle_type": VehicleType.VAN_MEDIUM,
    "brand": "Renault",
    "model": "Master",
    "energy_type": EnergyType.DIESEL,
    "max_weight_kg": 1500,
    "max_volume_m3": 12.0,
    "assigned_warehouses": [str(warehouse.id)]
})

print(f"Created vehicle: {vehicle.name}")
```

## Quick Tips

### List Resources

```python
# List all customers
customers = client.list_customers()
print(f"Total customers: {customers.count}")

# With filtering
active_customers = client.list_customers(is_active=True)
```

### Search

```python
# Search customers
results = client.list_customers(search="Company")

# Advanced filtering
locations = client.list_delivery_locations(
    city="Paris",
    has_coordinates=True,
    truck_access=True
)
```

### Error Handling

```python
from mapflow import NotFoundError, ValidationError

try:
    customer = client.get_customer(customer_id)
except NotFoundError:
    print("Customer not found")
except ValidationError as e:
    print(f"Validation error: {e.message}")
```

### Update Resources

```python
# Partial update
client.patch_customer(customer_id, {
    "notes": "Updated notes"
})

# Full update
client.update_customer(customer_id, {
    # ... all fields required
})
```

### Delete Resources

```python
client.delete_customer(customer_id)
```

## Next Steps

- Read the [full documentation](README.md)
- Check out [basic examples](examples/basic_usage.py)
- Explore [advanced features](examples/advanced_usage.py)
- Review the [API documentation](https://mapflow.readme.io/reference)

## Need Help?

- 📧 Email: support@mapflow.co
- 📚 Documentation: https://mapflow.readme.io/reference
- 🐛 Issues: https://github.com/mapflow/sdk-python/issues

## Common Patterns

### Bulk Operations

```python
# Activate multiple customers at once
client.customer_bulk_action(
    action="activate",
    customer_ids=[id1, id2, id3]
)
```

### Pagination

```python
page = 1
while True:
    response = client.list_customers(page=page)
    
    for customer in response.results:
        print(customer.display_name)
    
    if not response.next:
        break
    page += 1
```

### Using Global Customer API

Create customer, location, contact, and hours in one call:

```python
global_customer = client.create_global_customer({
    "customer_type": "company",
    "company_name": "Quick Start Corp",
    "delivery_location": {
        "name": "Main Office",
        "address": "123 Street",
        "zip_code": "75001",
        "city": "Paris",
        "country": "FR"
    },
    "contact": {
        "first_name": "John",
        "last_name": "Doe",
        "emails": ["john@example.com"]
    },
    "opening_hours": [
        {
            "day_of_week": 0,  # Monday
            "opening_time": "09:00",
            "closing_time": "18:00"
        }
    ]
})
```

Happy coding! 🚀

