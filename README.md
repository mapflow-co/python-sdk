# MapFlow Python SDK

**Official Python SDK for [MapFlow](https://mapflow.co) — Route Optimization & Delivery Management API**

[![PyPI version](https://img.shields.io/pypi/v/mapflow-sdk.svg)](https://pypi.org/project/mapflow-sdk/)
[![Python](https://img.shields.io/pypi/pyversions/mapflow-sdk.svg)](https://pypi.org/project/mapflow-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![API Docs](https://img.shields.io/badge/API-docs-green.svg)](https://mapflow.readme.io/reference)

MapFlow is a SaaS platform for route optimization, delivery planning, and logistics management. This SDK gives Python developers full programmatic access to the MapFlow API — manage customers, warehouses, drivers, vehicles, delivery schedules, and hierarchical product structures from your own applications.

→ **Website**: [https://mapflow.co](https://mapflow.co)  
→ **API Documentation**: [https://mapflow.readme.io/reference](https://mapflow.readme.io/reference)  
→ **Get your API key**: [https://mapflow.co](https://mapflow.co)

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [Core Resources](#core-resources)
  - [Customers](#customers)
  - [Delivery Locations](#delivery-locations)
  - [Warehouses](#warehouses)
  - [Drivers & Pickers](#drivers--pickers)
  - [Vehicles](#vehicles)
  - [Product Catalog](#product-catalog)
  - [Container Hierarchy (v2)](#container-hierarchy-v2)
  - [Visits & Scheduling](#visits--scheduling)
  - [Visit Products](#visit-products)
  - [Tags](#tags)
- [Pagination](#pagination)
- [Bulk Operations](#bulk-operations)
- [Error Handling](#error-handling)
- [Examples](#examples)
- [Support](#support)

---

## Features

- **Full API coverage** — customers, locations, warehouses, drivers, vehicles, catalog, visits, and more
- **Hierarchical product structures** — pallets containing packages containing products (v2)
- **Pydantic v2 models** — type-safe request/response objects with automatic validation
- **Paginated responses** — generic `PaginatedResponse[T]` with automatic deserialization
- **Bulk operations** — activate, deactivate, update, tag multiple records in one request
- **Flexible input** — pass Pydantic models or plain dicts to any write method
- **Rich error handling** — typed exceptions with HTTP status codes and API error details
- **Verbose mode** — built-in request/response logging for debugging
- **Python 3.8+** compatible

---

## Requirements

- Python ≥ 3.8
- `requests >= 2.31.0`
- `pydantic >= 2.0.0`

---

## Installation

```bash
pip install mapflow-sdk
```

Install from source:

```bash
git clone https://github.com/mapflow-co/python-sdk.git
cd python-sdk
pip install -e .
```

---

## Quick Start

```python
from mapflow import MapFlowClient, CustomerType, VisitType, ItemType

# Initialize the client
client = MapFlowClient(api_key="your-api-key")

# Create a customer
customer = client.create_customer({
    "customer_type": CustomerType.COMPANY,
    "company_name": "Acme Corp",
    "email": "contact@acme.com"
})

# Create a delivery location
location = client.create_delivery_location({
    "customer": str(customer.id),
    "name": "Main Office",
    "address": "42 Rue de la Paix",
    "zip_code": "75001",
    "city": "Paris"
})

# Schedule a delivery visit
visit = client.create_visit({
    "delivery_location": str(location.id),
    "visit_type": VisitType.DELIVERY,
    "visit_date": "2026-04-01"
})

print(f"Visit scheduled: {visit.id}")
```

---

## Authentication

All requests require an API key sent as the `X-API-Key` header. Get your key from your [MapFlow account](https://mapflow.co).

```python
client = MapFlowClient(
    api_key="your-api-key",          # required
    base_url="https://api.mapflow.co",  # optional — default shown
    timeout=30,                       # optional — seconds
    verbose=False                     # optional — logs requests/responses
)
```

---

## Core Resources

### Customers

Manage individual and business customers including billing details, VAT numbers, and SIRET.

```python
from mapflow import MapFlowClient, CustomerType

client = MapFlowClient(api_key="your-api-key")

# Create
customer = client.create_customer({
    "customer_type": CustomerType.COMPANY,
    "company_name": "Acme Corporation",
    "email": "contact@acme.com",
    "phone": "+33123456789",
    "billing_address": "123 Rue de la Paix",
    "billing_zip_code": "75001",
    "billing_city": "Paris",
    "billing_country": "FR",
    "siret": "12345678901234"
})

# List with filters
customers = client.list_customers(
    is_active=True,
    customer_type="company",
    search="Acme"
)
for c in customers.results:
    print(c.display_name, c.email)

# Read / Update / Delete
customer = client.get_customer(customer.id)
client.patch_customer(customer.id, {"notes": "VIP client"})
client.delete_customer(customer.id)

# Get all delivery locations for a customer
locations = client.get_customer_locations(customer.id)
```

### Delivery Locations

Physical addresses where deliveries or pickups take place, with geolocation and access constraints.

```python
location = client.create_delivery_location({
    "customer": str(customer.id),
    "name": "Main Warehouse",
    "address": "456 Avenue des Champs",
    "zip_code": "75008",
    "city": "Paris",
    "country": "FR",
    "latitude": 48.8566,
    "longitude": 2.3522,
    "truck_access": True,
    "loading_dock": True,
    "max_weight_kg": 5000
})

# Filter
locations = client.list_delivery_locations(city="Paris", truck_access=True)
```

**Global Customers** — create a customer, location, contact, and opening hours in a single atomic request:

```python
global_customer = client.create_global_customer({
    "customer_type": "company",
    "company_name": "Tech Solutions SARL",
    "email": "contact@techsolutions.fr",
    "delivery_location": {
        "name": "Head Office",
        "address": "10 Rue de la Tech",
        "zip_code": "69001",
        "city": "Lyon"
    },
    "contact": {
        "first_name": "Marie",
        "last_name": "Martin",
        "position": "Logistics Manager",
        "emails": ["marie@techsolutions.fr"],
        "is_primary": True
    },
    "opening_hours": [
        {"day_of_week": 0, "opening_time": "09:00", "closing_time": "18:00"},
        {"day_of_week": 1, "opening_time": "09:00", "closing_time": "18:00"}
    ]
})
```

### Warehouses

Operational bases for your fleet — supports start/end points, loading docks, certifications, and multi-vehicle assignment.

```python
from mapflow import WarehouseType

warehouse = client.create_warehouse({
    "name": "Paris Nord Hub",
    "code": "PARIS-01",
    "warehouse_type": WarehouseType.HUB,
    "address": "12 Rue Industrielle",
    "zip_code": "93200",
    "city": "Saint-Denis",
    "latitude": 48.9356,
    "longitude": 2.3539,
    "opening_time": "08:00",
    "closing_time": "18:00",
    "is_start_point": True,
    "is_end_point": True,
    "max_vehicles": 50
})

client.set_default_warehouse(warehouse.id)
```

### Drivers & Pickers

Manage drivers and warehouse order pickers with licence types, certifications, and vehicle capabilities.

```python
from mapflow import UserRole, DriverLicenceType, VehicleType

driver = client.create_driver_picker({
    "email": "driver@example.com",
    "first_name": "Jean",
    "last_name": "Dupont",
    "phone": "+33612345678",
    "role": UserRole.DRIVER,
    "password": "SecurePassword123!",
    "confirm_password": "SecurePassword123!",
    "has_valid_driving_license": True,
    "driver_licence_type": [DriverLicenceType.B, DriverLicenceType.C],
    "vehicle_types": [VehicleType.VAN_MEDIUM]
})

# Reset password
info = client.reset_driver_picker_password(driver.id)
```

### Vehicles

Fleet management including capacity, fuel type, maintenance status, and GPS tracking.

```python
from mapflow import VehicleType, EnergyType, VehicleStatus

vehicle = client.create_vehicle({
    "name": "Van 01",
    "license_plate": "AB-123-CD",
    "vehicle_type": VehicleType.VAN_MEDIUM,
    "brand": "Renault",
    "model": "Master",
    "year": 2023,
    "energy_type": EnergyType.DIESEL,
    "max_weight_kg": 1500,
    "max_volume_m3": 12.0,
    "status": VehicleStatus.AVAILABLE
})
```

### Product Catalog

Define products, services, packages, and pallets with weight, volume, pricing, and temperature constraints.

```python
from mapflow import ItemType, WeightUnit, VolumeUnit

product = client.create_delivery_item({
    "name": "Laptop Pro 16",
    "reference": "PROD-001",
    "item_type": ItemType.PRODUCT,
    "weight": 2.1,
    "weight_unit": WeightUnit.KG,
    "length": 36, "width": 25, "height": 2,
    "selling_price": 2499.00,
    "is_fragile": True
})

# Filter catalog
fragile = client.list_delivery_items(
    item_type=ItemType.PRODUCT,
    is_fragile=True,
    weight_max=5.0
)
```

### Container Hierarchy (v2)

Organize products inside packages and pallets with full nesting support, quantity tracking, and computed weight/value totals.

```python
# Create a pallet
pallet = client.create_delivery_item({
    "name": "Export Pallet EU",
    "item_type": ItemType.PALLET,
    "weight": 25, "weight_unit": WeightUnit.KG
})

# Create a package inside the pallet
box = client.create_delivery_item({
    "name": "Laptop Box",
    "item_type": ItemType.PACKAGE,
    "weight": 0.5, "weight_unit": WeightUnit.KG
})

# Put 5 laptops in the box
client.set_container_contents(box.id, [
    {"item": str(product.id), "quantity": 5, "notes": "Fragile"}
])

# Put 3 boxes on the pallet
client.set_container_contents(pallet.id, [
    {"item": str(box.id), "quantity": 3, "position": 1}
])

# Inspect the full hierarchy
hierarchy = client.get_delivery_item_hierarchy(pallet.id)
print(f"Total weight: {hierarchy.total_weight_kg} kg")
print(f"Total value: {hierarchy.total_selling_price} EUR")

# Granular removal
client.remove_content_from_container(pallet.id, box.id, quantity=1)

# List only top-level items (not inside any container)
roots = client.list_root_delivery_items()
```

### Visits & Scheduling

Schedule delivery, pickup, or service stops at delivery locations.

```python
from mapflow import VisitType

visit = client.create_visit({
    "delivery_location": str(location.id),
    "visit_type": VisitType.DELIVERY,
    "visit_date": "2026-04-01",
    "planned_start_time": "09:00",
    "planned_end_time": "10:00",
    "notes": "Ring bell at entrance"
})

# Filter visits
visits = client.list_visits(
    visit_date="2026-04-01",
    visit_type="delivery",
    status="planned"
)
```

### Visit Products

Link catalog items to a scheduled visit with quantities.

```python
# Assign a product to a visit
visit_product = client.create_visit_product({
    "visit": str(visit.id),
    "product": str(product.id),
    "quantity": 3
})

# Bulk quantity updates
client.visit_product_bulk_action(
    action="multiply_quantity",
    visitproduct_ids=[vp1.id, vp2.id],
    quantity_multiplier="2.0"
)
```

### Tags

Color-coded labels for visits, drivers, and customers.

```python
tag = client.create_tag({
    "name": "Urgent",
    "color": "#FF0000",
    "description": "Priority deliveries"
})

# Assign tags to customers in bulk
client.customer_bulk_action(
    action="add_tags",
    customer_ids=[c1.id, c2.id],
    tag_ids=[tag.id]
)
```

---

## Pagination

All list endpoints return a `PaginatedResponse[T]` with full IDE autocomplete on results.

```python
page = client.list_customers(page=1, page_size=20)

print(f"Total: {page.count}")
print(f"Pages: {page.total_pages}")

for customer in page.results:   # typed as List[Customer]
    print(customer.display_name)

# Iterate all pages
page_num = 1
while True:
    page = client.list_customers(page=page_num, page_size=50)
    for customer in page.results:
        process(customer)
    if not page.next:
        break
    page_num += 1
```

---

## Bulk Operations

Most resources support bulk actions to reduce round-trips.

```python
# Activate / deactivate
client.customer_bulk_action("activate", customer_ids=[id1, id2, id3])
client.vehicle_bulk_action("change_status", vehicle_ids=[v1, v2], new_status="maintenance")

# Bulk tagging
client.customer_bulk_action("add_tags", customer_ids=[id1, id2], tag_ids=[tag.id])

# Bulk product updates
client.delivery_item_bulk_action("update_fragile", delivery_item_ids=[p1, p2], is_fragile=True)
client.visit_product_bulk_action("update_quantity", visitproduct_ids=[vp1, vp2], new_quantity=5)
```

---

## Error Handling

The SDK raises typed exceptions for every HTTP error class.

```python
from mapflow import (
    MapFlowError,
    AuthenticationError,   # 401
    ForbiddenError,        # 403
    NotFoundError,         # 404
    ValidationError,       # 400
    RateLimitError,        # 429
    ServerError            # 5xx
)

try:
    customer = client.get_customer(customer_id)
except AuthenticationError:
    print("Invalid API key — check your credentials at https://mapflow.co")
except NotFoundError:
    print("Customer not found")
except ValidationError as e:
    print(f"Validation error: {e.message}")
    print(f"Details: {e.response}")
except RateLimitError:
    print("Rate limit exceeded — slow down requests")
except ServerError:
    print("MapFlow server error — try again later")
except MapFlowError as e:
    print(f"Error {e.status_code}: {e.message}")
```

---

## Examples

The `examples/` directory contains ready-to-run scripts:

| File | Description |
|------|-------------|
| `examples/hierarchy_example.py` | Pallets, packages, and products with quantities |
| `examples/visit_products_example.py` | Assigning catalog items to delivery visits |

Run any example after setting your API key:

```bash
export MAPFLOW_API_KEY="your-api-key"
python examples/hierarchy_example.py
```

---

## Enums Reference

| Enum | Values |
|------|--------|
| `CustomerType` | `individual`, `company` |
| `ItemType` | `PRODUCT`, `SERVICE`, `PACKAGE`, `PALLET` |
| `VisitType` | `delivery`, `pickup`, `service`, `delivery_pickup` |
| `VehicleType` | `bicycle`, `cargo_bike`, `motorcycle`, `van_small`, `van_medium`, `van_large`, `truck_small`, `truck_medium`, `truck_large`, `semi_trailer`, `refrigerated`, … |
| `VehicleStatus` | `available`, `in_use`, `maintenance`, `broken`, `retired` |
| `EnergyType` | `gasoline`, `diesel`, `electric`, `hybrid`, `hydrogen` |
| `DriverLicenceType` | `none`, `am`, `a1`, `a`, `b`, `c1`, `c`, `ce`, `d` |
| `WarehouseType` | `distribution`, `storage`, `hub`, `pickup`, `cross_dock`, `other` |
| `WeightUnit` | `kg`, `g`, `lb`, `oz`, `t` |
| `VolumeUnit` | `m3`, `l`, `ml`, `cm3`, `ft3`, `gal` |
| `DayOfWeek` | `MONDAY` (0) … `SUNDAY` (6) |

---

## Support

- **Website**: [https://mapflow.co](https://mapflow.co)
- **API Documentation**: [https://mapflow.readme.io/reference](https://mapflow.readme.io/reference)
- **Email**: support@mapflow.co
- **GitHub Issues**: [https://github.com/mapflow-co/python-sdk/issues](https://github.com/mapflow-co/python-sdk/issues)

---

## License

[MIT](LICENSE) © [MapFlow](https://mapflow.co)
