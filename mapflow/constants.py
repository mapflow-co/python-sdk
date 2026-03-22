"""Constants and enums for MapFlow SDK."""

from enum import Enum


# API Configuration
DEFAULT_BASE_URL = "https://api.mapflow.co"
API_VERSION = "v1"


# Customer Types
class CustomerType(str, Enum):
    """Customer type enumeration."""
    INDIVIDUAL = "individual"
    COMPANY = "company"


# Item Types
class ItemType(str, Enum):
    """Delivery item type enumeration."""
    PRODUCT = "PRODUCT"
    SERVICE = "SERVICE"
    PACKAGE = "PACKAGE"
    PALLET = "PALLET"


# Weight Units
class WeightUnit(str, Enum):
    """Weight unit enumeration."""
    KG = "kg"
    G = "g"
    LB = "lb"
    OZ = "oz"
    T = "t"


# Volume Units
class VolumeUnit(str, Enum):
    """Volume unit enumeration."""
    M3 = "m3"
    L = "l"
    ML = "ml"
    CM3 = "cm3"
    FT3 = "ft3"
    GAL = "gal"


# Duration Units
class DurationUnit(str, Enum):
    """Duration unit enumeration."""
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"


# Day of Week
class DayOfWeek(int, Enum):
    """Day of week enumeration."""
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


# Vehicle Types
class VehicleType(str, Enum):
    """Vehicle type enumeration."""
    BICYCLE = "bicycle"
    CARGO_BIKE = "cargo_bike"
    ELECTRIC_SCOOTER = "electric_scooter"
    SCOOTER_50 = "scooter_50"
    SCOOTER_125 = "scooter_125"
    MOTORCYCLE = "motorcycle"
    CAR = "car"
    VAN_SMALL = "van_small"
    VAN_MEDIUM = "van_medium"
    VAN_LARGE = "van_large"
    VAN_XL = "van_xl"
    TRUCK_SMALL = "truck_small"
    TRUCK_MEDIUM = "truck_medium"
    TRUCK_LARGE = "truck_large"
    TRUCK_XL = "truck_xl"
    TRUCK_TRAILER = "truck_trailer"
    SEMI_TRAILER = "semi_trailer"
    REFRIGERATED = "refrigerated"
    TANKER = "tanker"
    FLATBED = "flatbed"
    OTHER = "other"


# Energy Types
class EnergyType(str, Enum):
    """Energy type enumeration."""
    GASOLINE = "gasoline"
    DIESEL = "diesel"
    ELECTRIC = "electric"
    HYBRID = "hybrid"
    HYDROGEN = "hydrogen"


# Vehicle Status
class VehicleStatus(str, Enum):
    """Vehicle status enumeration."""
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"
    BROKEN = "broken"
    IMPOUNDED = "impounded"
    IMMOBILIZED = "immobilized"
    RETIRED = "retired"


# Driver Licence Types
class DriverLicenceType(str, Enum):
    """Driver licence type enumeration."""
    NONE = "none"
    AM = "am"
    A1 = "a1"
    A = "a"
    B = "b"
    C1 = "c1"
    C = "c"
    CE = "ce"
    D = "d"


# Warehouse Types
class WarehouseType(str, Enum):
    """Warehouse type enumeration."""
    DISTRIBUTION = "distribution"
    STORAGE = "storage"
    HUB = "hub"
    PICKUP = "pickup"
    CROSS_DOCK = "cross_dock"
    OTHER = "other"


# User Roles
class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    MANAGER = "manager"
    DISPATCHER = "dispatcher"
    DRIVER = "driver"
    ORDER_PICKER = "order_picker"
    CUSTOMER_SERVICE = "customer_service"
    ANALYST = "analyst"
    VIEWER = "viewer"


# Departments
class Department(str, Enum):
    """Department enumeration."""
    LOGISTICS = "logistics"
    DELIVERY = "delivery"
    WAREHOUSE = "warehouse"
    CUSTOMER_SERVICE = "customer_service"
    MANAGEMENT = "management"
    MAINTENANCE = "maintenance"
    PLANNING = "planning"


# Languages
class Language(str, Enum):
    """Language enumeration."""
    FRENCH = "fr"
    ENGLISH = "en"
    SPANISH = "es"
    GERMAN = "de"


# Warehouse Certifications
class WarehouseCertification(str, Enum):
    """Warehouse certification enumeration."""
    CACES_1 = "caces_1"
    CACES_2 = "caces_2"
    CACES_3 = "caces_3"
    CACES_4 = "caces_4"
    CACES_5 = "caces_5"
    CACES_7 = "caces_7"
    CACES_NACELLE = "caces_nacelle"
    CACES_GRUE_MOBILE = "caces_grue_mobile"
    CACES_GRUE_TOUR = "caces_grue_tour"


# KM Source
class KmSource(str, Enum):
    """Kilometer source enumeration."""
    MANUAL = "manual"
    GPS = "gps"
    OBD = "obd"
    FUEL = "fuel"


# Visit Types
class VisitType(str, Enum):
    """Visit type enumeration."""
    DELIVERY = "delivery"
    PICKUP = "pickup"
    SERVICE = "service"
    DELIVERY_PICKUP = "delivery_pickup"

