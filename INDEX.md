# MapFlow Python SDK - Documentation Index

Welcome to the MapFlow Python SDK! This index helps you find the right documentation for your needs.

## 🚀 Getting Started

**New to MapFlow SDK?** Start here:

1. **[QUICKSTART.md](QUICKSTART.md)** - Get up and running in 5 minutes
2. **[examples/getting_started.py](examples/getting_started.py)** - Interactive setup script
3. **[README.md](README.md)** - Complete introduction and overview

## 📚 Core Documentation

### For Users

- **[README.md](README.md)** - Main documentation with examples
  - Installation instructions
  - Basic usage examples
  - Configuration guide
  - Error handling
  - All major features

- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
  - 5-minute setup
  - First customer, location, warehouse
  - Basic operations
  - Common tips

- **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API reference
  - All client methods documented
  - Parameter descriptions
  - Return types
  - Examples for each method

- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Usage patterns and best practices
  - Dictionary vs Pydantic models
  - Enum usage
  - Pagination strategies
  - Error handling patterns
  - Performance tips
  - Security best practices

### For Developers

- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development guide
  - Project structure
  - Development setup
  - Adding new features
  - Testing strategy
  - Release process

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
  - How to contribute
  - Code style
  - Pull request process
  - Running tests

- **[SDK_OVERVIEW.md](SDK_OVERVIEW.md)** - Technical overview
  - Architecture diagram
  - Component descriptions
  - Data flow
  - Design principles

## 📝 Examples

### Basic Examples

- **[examples/basic_usage.py](examples/basic_usage.py)**
  - Customer CRUD operations
  - Location management
  - Warehouse setup
  - Product catalog
  - Vehicle management
  - Tag creation

### Advanced Examples

- **[examples/advanced_usage.py](examples/advanced_usage.py)**
  - Error handling patterns
  - Global customer API
  - Bulk operations
  - Advanced search
  - Pagination handling
  - Complex queries

### Integration Examples

- **[examples/integration_example.py](examples/integration_example.py)**
  - Import customer data from external system
  - Create delivery locations
  - Set up warehouses
  - Import product catalog
  - Export data
  - Sync with external system

### Workflow Examples

- **[examples/common_workflows.py](examples/common_workflows.py)**
  - Onboard new customer
  - Setup vehicle fleet
  - Organize product catalog
  - Find and update resources
  - Generate reports
  - Data migration

### Other Examples

- **[examples/validation_example.py](examples/validation_example.py)** - Data validation
- **[examples/demo.py](examples/demo.py)** - Interactive demo

## 🔍 Find What You Need

### I want to...

**...install the SDK**
→ [README.md - Installation](README.md#installation)

**...get my API key**
→ [QUICKSTART.md - Step 1](QUICKSTART.md#get-your-api-key)

**...create my first customer**
→ [QUICKSTART.md - Create Customer](QUICKSTART.md#2-create-your-first-customer)

**...understand all available methods**
→ [API_REFERENCE.md](API_REFERENCE.md)

**...see code examples**
→ [examples/](examples/) directory

**...handle errors properly**
→ [USAGE_GUIDE.md - Error Handling](USAGE_GUIDE.md#error-handling-strategies)

**...use bulk operations**
→ [README.md - Bulk Actions](README.md#actions-en-lot-bulk-actions)

**...validate data before sending**
→ [examples/validation_example.py](examples/validation_example.py)

**...understand pagination**
→ [USAGE_GUIDE.md - Pagination](USAGE_GUIDE.md#pagination-patterns)

**...integrate with my existing system**
→ [examples/integration_example.py](examples/integration_example.py)

**...contribute to the SDK**
→ [CONTRIBUTING.md](CONTRIBUTING.md)

**...see what changed in each version**
→ [CHANGELOG.md](CHANGELOG.md)

## 📊 Quick Reference

### Most Used Methods

```python
# Customers
client.list_customers(**filters)
client.create_customer(data)
client.get_customer(customer_id)
client.patch_customer(customer_id, updates)

# Locations
client.list_delivery_locations(**filters)
client.create_delivery_location(data)
client.get_delivery_location(location_id)

# Warehouses
client.list_warehouses(**filters)
client.create_warehouse(data)
client.set_default_warehouse(warehouse_id)

# Catalog
client.list_delivery_items(**filters)
client.create_delivery_item(data)

# Vehicles
client.list_vehicles(**filters)
client.create_vehicle(data)

# Bulk Operations
client.customer_bulk_action(action, ids, **params)
client.delivery_item_bulk_action(action, ids, **params)
client.vehicle_bulk_action(action, ids, **params)
```

### Most Used Models

```python
from mapflow import (
    CustomerCreate,
    DeliveryLocationCreate,
    WarehouseCreate,
    DeliveryItemCreate,
    VehicleCreate,
    TagCreate
)
```

### Most Used Enums

```python
from mapflow import (
    CustomerType,      # INDIVIDUAL, COMPANY
    ItemType,          # PRODUCT, SERVICE, PACKAGE, PALLET
    VehicleType,       # VAN_SMALL, VAN_MEDIUM, TRUCK_SMALL, etc.
    WarehouseType,     # DISTRIBUTION, STORAGE, HUB, etc.
    WeightUnit,        # KG, G, LB, etc.
    VolumeUnit         # M3, L, ML, etc.
)
```

## 🧪 Testing & Verification

- **[run_tests.py](run_tests.py)** - Run all unit tests
- **[verify_installation.py](verify_installation.py)** - Verify installation
- **[tests/](tests/)** - Test suite

## 📦 Package Files

- **[setup.py](setup.py)** - Package setup configuration
- **[pyproject.toml](pyproject.toml)** - Modern Python packaging
- **[requirements.txt](requirements.txt)** - Dependencies
- **[MANIFEST.in](MANIFEST.in)** - Package manifest
- **[LICENSE](LICENSE)** - MIT License

## 🆘 Support

- 📧 Email: support@mapflow.co
- 📚 API Docs: https://mapflow.readme.io/reference
- 🐛 Issues: https://github.com/mapflow/sdk-python/issues
- 💬 Discussions: https://github.com/mapflow/sdk-python/discussions

## 🗺️ Navigation Tips

1. **Beginner?** → QUICKSTART.md → examples/basic_usage.py
2. **Need reference?** → API_REFERENCE.md
3. **Integration project?** → examples/integration_example.py → USAGE_GUIDE.md
4. **Contributing?** → CONTRIBUTING.md → DEVELOPMENT.md
5. **Troubleshooting?** → USAGE_GUIDE.md (Troubleshooting section)

## 📋 Checklist for New Users

- [ ] Install SDK: `pip install mapflow-co-sdk`
- [ ] Get API key from MapFlow dashboard
- [ ] Run: `python verify_installation.py`
- [ ] Read: QUICKSTART.md
- [ ] Try: examples/getting_started.py
- [ ] Explore: examples/basic_usage.py
- [ ] Build: Your integration!

---

**Last Updated:** January 2024  
**SDK Version:** 1.0.0  
**Python Version:** >=3.8

