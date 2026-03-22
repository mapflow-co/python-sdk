"""
MapFlow Python SDK
==================

Python SDK for MapFlow route optimization API.

Version 2.0.0 adds support for hierarchical product structures:
- Palettes containing packages and products
- Packages containing products and services
- Container contents with quantities

Basic usage:
    >>> from mapflow import MapFlowClient
    >>> client = MapFlowClient(api_key="your-api-key")
    >>> customers = client.list_customers()

Hierarchical products (v2):
    >>> # Create a pallet with nested products
    >>> pallet = client.create_delivery_item({
    ...     "name": "Palette Export",
    ...     "item_type": "PALLET"
    ... })
    >>> # Add products with quantities
    >>> client.set_container_contents(pallet.id, [
    ...     {"item": str(product_id), "quantity": 5}
    ... ])

For more information, visit https://api.mapflow.co/docs
"""

__version__ = "2.0.0"

from .client import MapFlowClient
from .exceptions import (
    MapFlowError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    ForbiddenError,
    ServerError,
    RateLimitError
)
from .constants import (
    DEFAULT_BASE_URL,
    CustomerType,
    ItemType,
    WeightUnit,
    VolumeUnit,
    DurationUnit,
    DayOfWeek,
    VehicleType,
    EnergyType,
    VehicleStatus,
    DriverLicenceType,
    WarehouseType,
    UserRole,
    Department,
    Language,
    WarehouseCertification,
    KmSource,
    VisitType
)
from .models import (
    Customer,
    CustomerCreate,
    CustomerUpdate,
    DeliveryLocation,
    DeliveryLocationCreate,
    DeliveryLocationUpdate,
    Warehouse,
    WarehouseCreate,
    WarehouseUpdate,
    GlobalCustomer,
    GlobalCustomerCreate,
    LocationContact,
    LocationContactCreate,
    LocationContactUpdate,
    LocationOpeningHours,
    LocationOpeningHoursCreate,
    LocationOpeningHoursUpdate,
    # Container Content Models (v2)
    ContainerContent,
    ContainerContentCreate,
    ContainerContentItemDetail,
    # Delivery Item Models (v2)
    DeliveryItem,
    DeliveryItemCreate,
    DeliveryItemUpdate,
    # Other Models
    DriverPicker,
    DriverPickerCreate,
    DriverPickerUpdate,
    Vehicle,
    VehicleCreate,
    VehicleUpdate,
    Tag,
    TagCreate,
    TagUpdate,
    Visit,
    VisitCreate,
    VisitUpdate,
    VisitProduct,
    VisitProductCreate,
    VisitProductUpdate,
    PaginatedResponse
)

__all__ = [
    # Client
    "MapFlowClient",
    
    # Exceptions
    "MapFlowError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "ForbiddenError",
    "ServerError",
    "RateLimitError",
    
    # Constants
    "DEFAULT_BASE_URL",
    "CustomerType",
    "ItemType",
    "WeightUnit",
    "VolumeUnit",
    "DurationUnit",
    "DayOfWeek",
    "VehicleType",
    "EnergyType",
    "VehicleStatus",
    "DriverLicenceType",
    "WarehouseType",
    "UserRole",
    "Department",
    "Language",
    "WarehouseCertification",
    "KmSource",
    "VisitType",
    
    # Models - Customers
    "Customer",
    "CustomerCreate",
    "CustomerUpdate",
    
    # Models - Delivery Locations
    "DeliveryLocation",
    "DeliveryLocationCreate",
    "DeliveryLocationUpdate",
    
    # Models - Warehouses
    "Warehouse",
    "WarehouseCreate",
    "WarehouseUpdate",
    
    # Models - Global Customers
    "GlobalCustomer",
    "GlobalCustomerCreate",
    
    # Models - Contacts
    "LocationContact",
    "LocationContactCreate",
    "LocationContactUpdate",
    
    # Models - Opening Hours
    "LocationOpeningHours",
    "LocationOpeningHoursCreate",
    "LocationOpeningHoursUpdate",
    
    # Models - Container Contents (v2)
    "ContainerContent",
    "ContainerContentCreate",
    "ContainerContentItemDetail",
    
    # Models - Delivery Items (v2)
    "DeliveryItem",
    "DeliveryItemCreate",
    "DeliveryItemUpdate",
    
    # Models - Drivers/Pickers
    "DriverPicker",
    "DriverPickerCreate",
    "DriverPickerUpdate",
    
    # Models - Vehicles
    "Vehicle",
    "VehicleCreate",
    "VehicleUpdate",
    
    # Models - Tags
    "Tag",
    "TagCreate",
    "TagUpdate",
    
    # Models - Visits
    "Visit",
    "VisitCreate",
    "VisitUpdate",
    
    # Models - Visit Products
    "VisitProduct",
    "VisitProductCreate",
    "VisitProductUpdate",
    
    # Models - Pagination
    "PaginatedResponse",
]

