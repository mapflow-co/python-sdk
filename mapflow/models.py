"""Pydantic models for MapFlow SDK."""

from __future__ import annotations

from datetime import datetime, date, time
from decimal import Decimal
from typing import Optional, List, Dict, Any, Union, TypeVar, Generic
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator

from .constants import (
    CustomerType, ItemType, WeightUnit, VolumeUnit, DurationUnit,
    DayOfWeek, VehicleType, EnergyType, VehicleStatus, DriverLicenceType,
    WarehouseType, UserRole, Department, Language, WarehouseCertification,
    KmSource, VisitType
)


# ============================================================================
# Base Models
# ============================================================================

class MapFlowBaseModel(BaseModel):
    """Base model with common configuration."""
    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


# ============================================================================
# Customer Models
# ============================================================================

class CustomerBase(MapFlowBaseModel):
    """Base customer model."""
    customer_type: CustomerType
    email: Optional[str] = None
    phone: Optional[str] = None
    emails: Optional[List[str]] = None
    phones: Optional[List[str]] = None
    company_name: Optional[str] = None
    siret: Optional[str] = None
    vat_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    billing_address: Optional[str] = None
    billing_zip_code: Optional[str] = None
    billing_city: Optional[str] = None
    billing_country: Optional[str] = None
    external_id: Optional[str] = None
    external_reference: Optional[str] = None
    is_active: bool = True
    notes: Optional[str] = None


class CustomerCreate(CustomerBase):
    """Model for creating a customer."""
    pass


class CustomerUpdate(CustomerBase):
    """Model for updating a customer."""
    pass


class Customer(CustomerBase):
    """Complete customer model."""
    id: Optional[UUID] = None
    organisation: Optional[UUID] = None
    organisation_name: Optional[str] = None
    display_name: Optional[str] = None
    location_count: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ============================================================================
# Delivery Location Models
# ============================================================================

class DeliveryLocationBase(MapFlowBaseModel):
    """Base delivery location model."""
    customer: UUID
    name: str
    reference: Optional[str] = None
    address: str
    zip_code: str
    city: str
    country: Optional[str] = "FR"
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    delivery_instructions: Optional[str] = None
    access_instructions: Optional[str] = None
    special_equipment_required: Optional[str] = None
    max_weight_kg: Optional[int] = None
    max_volume_m3: Optional[Decimal] = None
    truck_access: bool = False
    loading_dock: bool = False
    elevator_access: bool = False
    floor_level: Optional[int] = None
    is_active: bool = True
    internal_notes: Optional[str] = None


class DeliveryLocationCreate(DeliveryLocationBase):
    """Model for creating a delivery location."""
    pass


class DeliveryLocationUpdate(DeliveryLocationBase):
    """Model for updating a delivery location."""
    external_id: Optional[str] = None
    external_reference: Optional[str] = None


class DeliveryLocation(DeliveryLocationBase):
    """Complete delivery location model."""
    id: Optional[UUID] = None
    customer_name: Optional[str] = None
    customer_display_name: Optional[str] = None
    full_address: Optional[str] = None
    has_coordinates: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ============================================================================
# Warehouse Models
# ============================================================================

class WarehouseBase(MapFlowBaseModel):
    """Base warehouse model."""
    name: str
    code: Optional[str] = None
    warehouse_type: Optional[WarehouseType] = None
    address: str
    zip_code: str
    city: str
    country: Optional[str] = "FR"
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    saturday_opening: Optional[time] = None
    saturday_closing: Optional[time] = None
    sunday_opening: Optional[time] = None
    sunday_closing: Optional[time] = None
    max_capacity_m3: Optional[Decimal] = None
    max_weight_capacity_kg: Optional[int] = None
    max_vehicles: Optional[int] = None
    has_loading_dock: bool = False
    has_forklift: bool = False
    has_crane: bool = False
    has_cold_storage: bool = False
    has_security: bool = False
    has_parking: bool = False
    is_start_point: bool = True
    is_end_point: bool = True
    is_break_point: bool = False
    cost_per_hour: Optional[Decimal] = None
    cost_per_m3: Optional[Decimal] = None
    is_active: bool = True
    is_default: bool = False
    access_instructions: Optional[str] = None
    loading_instructions: Optional[str] = None
    special_requirements: Optional[str] = None
    internal_notes: Optional[str] = None


class WarehouseCreate(WarehouseBase):
    """Model for creating a warehouse."""
    pass


class WarehouseUpdate(WarehouseBase):
    """Model for updating a warehouse."""
    pass


class Warehouse(WarehouseBase):
    """Complete warehouse model."""
    id: Optional[UUID] = None
    organisation: Optional[UUID] = None
    organisation_name: Optional[str] = None
    full_address: Optional[str] = None
    has_coordinates: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ============================================================================
# Global Customer Models
# ============================================================================

class GlobalCustomerBase(MapFlowBaseModel):
    """Base global customer model."""
    customer_type: CustomerType
    email: Optional[str] = None
    phone: Optional[str] = None
    emails: Optional[List[str]] = None
    phones: Optional[List[str]] = None
    company_name: Optional[str] = None
    siret: Optional[str] = None
    vat_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    billing_address: Optional[str] = None
    billing_zip_code: Optional[str] = None
    billing_city: Optional[str] = None
    billing_country: Optional[str] = "FR"
    external_reference: Optional[str] = None
    external_id: Optional[str] = None
    is_active: bool = True
    notes: Optional[str] = None
    delivery_location: Optional[Dict[str, Any]] = None
    contact: Optional[Dict[str, Any]] = None
    opening_hours: Optional[List[Dict[str, Any]]] = None


class GlobalCustomerCreate(GlobalCustomerBase):
    """Model for creating a global customer."""
    delivery_location: Dict[str, Any]


class GlobalCustomer(GlobalCustomerBase):
    """Complete global customer model."""
    id: UUID  # ID de la DeliveryLocation (utilisé pour les opérations GET/PUT/PATCH/DELETE)
    customer_id: Optional[UUID] = None  # ID du Customer (pour référence)
    display_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,  # Important : permet d'accepter à la fois 'id' et 'customer_id'
        arbitrary_types_allowed=True
    )


# ============================================================================
# Contact Models
# ============================================================================

class LocationContactBase(MapFlowBaseModel):
    """Base location contact model."""
    first_name: str
    last_name: str
    position: Optional[str] = None
    emails: Optional[List[str]] = None
    phones: Optional[List[str]] = None
    is_primary: bool = False
    is_active: bool = True
    notes: Optional[str] = None


class LocationContactCreate(LocationContactBase):
    """Model for creating a location contact."""
    location_ids: List[UUID]


class LocationContactUpdate(LocationContactBase):
    """Model for updating a location contact."""
    location_ids: Optional[List[UUID]] = None


class LocationContact(LocationContactBase):
    """Complete location contact model."""
    id: UUID
    full_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# ============================================================================
# Opening Hours Models
# ============================================================================

class LocationOpeningHoursBase(MapFlowBaseModel):
    """Base location opening hours model."""
    location: UUID
    day_of_week: DayOfWeek
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    is_closed: bool = False
    break_start: Optional[time] = None
    break_end: Optional[time] = None
    notes: Optional[str] = None


class LocationOpeningHoursCreate(LocationOpeningHoursBase):
    """Model for creating opening hours."""
    pass


class LocationOpeningHoursUpdate(MapFlowBaseModel):
    """Model for updating opening hours."""
    day_of_week: DayOfWeek
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    is_closed: bool = False
    break_start: Optional[time] = None
    break_end: Optional[time] = None
    notes: Optional[str] = None


class LocationOpeningHours(LocationOpeningHoursBase):
    """Complete opening hours model."""
    id: UUID
    location_name: Optional[str] = None
    day_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# ============================================================================
# Container Content Models (v2 - Hierarchical support)
# ============================================================================

class ContainerContentItemDetail(MapFlowBaseModel):
    """Détails compacts de l'item dans un contenu de conteneur."""
    id: UUID
    reference: Optional[str] = None
    name: str
    item_type: ItemType
    weight_kg: Optional[Decimal] = None
    volume_m3: Optional[Decimal] = None


class ContainerContent(MapFlowBaseModel):
    """Contenu d'un conteneur avec quantité."""
    id: UUID
    container: UUID
    item: UUID
    item_id: Optional[UUID] = None
    item_name: Optional[str] = None
    item_reference: Optional[str] = None
    item_type: Optional[ItemType] = None
    item_type_display: Optional[str] = None
    item_details: Optional[ContainerContentItemDetail] = None
    quantity: int
    position: int = 0
    notes: Optional[str] = None
    # Caractéristiques unitaires
    item_weight_kg: Optional[Decimal] = None
    item_volume_m3: Optional[Decimal] = None
    item_declared_value: Optional[Decimal] = None
    item_buying_price: Optional[Decimal] = None
    item_selling_price: Optional[Decimal] = None
    # Totaux avec quantité
    total_weight_kg: Optional[Decimal] = None
    total_volume_m3: Optional[Decimal] = None
    total_declared_value: Optional[Decimal] = None
    total_buying_price: Optional[Decimal] = None
    total_selling_price: Optional[Decimal] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ContainerContentCreate(MapFlowBaseModel):
    """Modèle pour créer un contenu de conteneur."""
    item: UUID
    quantity: int = 1
    position: int = 0
    notes: Optional[str] = None


# ============================================================================
# Delivery Item Models
# ============================================================================

class DeliveryItemBase(MapFlowBaseModel):
    """Base delivery item model."""
    reference: Optional[str] = None
    name: str
    description: Optional[str] = None
    item_type: ItemType
    barcode: Optional[str] = None
    external_id: Optional[str] = None
    external_reference: Optional[str] = None
    weight: Optional[Decimal] = Field(None, ge=0)
    weight_unit: Optional[WeightUnit] = WeightUnit.KG
    length: Optional[Decimal] = Field(None, ge=0)
    width: Optional[Decimal] = Field(None, ge=0)
    height: Optional[Decimal] = Field(None, ge=0)
    volume: Optional[Decimal] = Field(None, ge=0)
    volume_unit: Optional[VolumeUnit] = VolumeUnit.M3
    temperature_min: Optional[Decimal] = None
    temperature_max: Optional[Decimal] = None
    is_fragile: bool = False
    is_dangerous: bool = False
    is_biohazard: bool = False
    declared_value: Optional[Decimal] = Field(None, ge=0)
    currency: str = "EUR"
    buying_price: Optional[Decimal] = Field(None, ge=0)
    selling_price: Optional[Decimal] = Field(None, ge=0)
    vat_rate: Optional[Decimal] = Field(None, ge=0, le=100)
    estimated_delivery_duration: int = 0
    estimated_delivery_duration_unit: DurationUnit = DurationUnit.MINUTES
    package_code: Optional[str] = None
    number_of_packages: int = 1
    tags: Optional[List[UUID]] = None
    
    @field_validator('buying_price', 'selling_price', 'declared_value', mode='before')
    @classmethod
    def validate_non_negative_prices(cls, v):
        """Valide que les prix ne sont pas négatifs."""
        if v is not None:
            try:
                v_float = float(v)
                if v_float < 0:
                    raise ValueError('Les prix ne peuvent pas être négatifs')
            except (ValueError, TypeError):
                raise ValueError(f'Prix invalide : {v}')
        return v

    @field_validator('vat_rate', mode='before')
    @classmethod
    def validate_vat_rate(cls, v):
        """Valide que le taux de TVA est entre 0 et 100."""
        if v is not None:
            try:
                v_float = float(v)
                if v_float < 0 or v_float > 100:
                    raise ValueError('Le taux de TVA doit être compris entre 0 et 100')
            except (ValueError, TypeError):
                raise ValueError(f'Taux de TVA invalide : {v}')
        return v
    
    @model_validator(mode='after')
    def validate_temperature_range(self):
        """Valide que la température minimale n'est pas supérieure à la maximale."""
        if self.temperature_min is not None and self.temperature_max is not None:
            if self.temperature_min > self.temperature_max:
                raise ValueError('La température minimale ne peut pas être supérieure à la température maximale')
        return self


class DeliveryItemCreate(DeliveryItemBase):
    """Model for creating a delivery item."""
    pass


class DeliveryItemUpdate(MapFlowBaseModel):
    """Model for updating a delivery item (all fields optional for partial updates)."""
    reference: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    item_type: Optional[ItemType] = None
    barcode: Optional[str] = None
    external_id: Optional[str] = None
    external_reference: Optional[str] = None
    weight: Optional[Decimal] = Field(None, ge=0)
    weight_unit: Optional[WeightUnit] = None
    length: Optional[Decimal] = Field(None, ge=0)
    width: Optional[Decimal] = Field(None, ge=0)
    height: Optional[Decimal] = Field(None, ge=0)
    volume: Optional[Decimal] = Field(None, ge=0)
    volume_unit: Optional[VolumeUnit] = None
    temperature_min: Optional[Decimal] = None
    temperature_max: Optional[Decimal] = None
    is_fragile: Optional[bool] = None
    is_dangerous: Optional[bool] = None
    is_biohazard: Optional[bool] = None
    declared_value: Optional[Decimal] = Field(None, ge=0)
    currency: Optional[str] = None
    buying_price: Optional[Decimal] = Field(None, ge=0)
    selling_price: Optional[Decimal] = Field(None, ge=0)
    vat_rate: Optional[Decimal] = Field(None, ge=0, le=100)
    estimated_delivery_duration: Optional[int] = None
    estimated_delivery_duration_unit: Optional[DurationUnit] = None
    package_code: Optional[str] = None
    number_of_packages: Optional[int] = None
    tags: Optional[List[UUID]] = None
    
    @field_validator('buying_price', 'selling_price', 'declared_value', mode='before')
    @classmethod
    def validate_non_negative_prices(cls, v):
        """Valide que les prix ne sont pas négatifs."""
        if v is not None:
            try:
                v_float = float(v)
                if v_float < 0:
                    raise ValueError('Les prix ne peuvent pas être négatifs')
            except (ValueError, TypeError):
                raise ValueError(f'Prix invalide : {v}')
        return v

    @field_validator('vat_rate', mode='before')
    @classmethod
    def validate_vat_rate(cls, v):
        """Valide que le taux de TVA est entre 0 et 100."""
        if v is not None:
            try:
                v_float = float(v)
                if v_float < 0 or v_float > 100:
                    raise ValueError('Le taux de TVA doit être compris entre 0 et 100')
            except (ValueError, TypeError):
                raise ValueError(f'Taux de TVA invalide : {v}')
        return v
    
    @model_validator(mode='after')
    def validate_temperature_range(self):
        """Valide que la température minimale n'est pas supérieure à la maximale."""
        if self.temperature_min is not None and self.temperature_max is not None:
            if self.temperature_min > self.temperature_max:
                raise ValueError('La température minimale ne peut pas être supérieure à la température maximale')
        return self


class DeliveryItem(DeliveryItemBase):
    """
    Complete delivery item model with container support (v2).
    
    Les conteneurs (PALLET, PACKAGE) peuvent contenir d'autres éléments
    via le champ `contents` qui utilise ContainerContent avec quantités.
    """
    id: UUID
    organisation: Optional[UUID] = None
    organisation_name: Optional[str] = None
    weight_display: Optional[str] = None
    weight_kg: Optional[Decimal] = None
    volume_display: Optional[str] = None
    volume_m3: Optional[Decimal] = None
    calculated_volume_m3: Optional[Decimal] = None
    temperature_range: Optional[str] = None
    has_temperature_constraints: Optional[bool] = None
    has_constraints: Optional[bool] = None
    priority_score: Optional[Decimal] = None
    validation_requirements: Optional[List[str]] = None
    selling_price_all_taxes_included: Optional[Decimal] = None
    buying_price_all_taxes_included: Optional[Decimal] = None
    created_at: datetime
    updated_at: datetime
    
    # Champs de conteneur (v2 - simplifié)
    depth_level: int = 0
    is_root: bool = True
    is_container: bool = False
    
    # Champs de contenus avec quantités (v2)
    contents_count: int = 0
    total_items_quantity: int = 0
    contents: List[ContainerContent] = []
    
    # Totaux calculés automatiquement (v2)
    total_weight_kg: Optional[Decimal] = None
    total_volume_m3: Optional[Decimal] = None
    total_declared_value: Optional[Decimal] = None
    total_buying_price: Optional[Decimal] = None
    total_selling_price: Optional[Decimal] = None


# Mise à jour des forward references pour les modèles récursifs
DeliveryItem.model_rebuild()


# ============================================================================
# Driver/Picker Models
# ============================================================================

class DriverPickerBase(MapFlowBaseModel):
    """Base driver/picker model."""
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    department: Optional[Department] = None
    employee_id: Optional[str] = None
    timezone: Optional[str] = "Europe/Paris"
    language: Optional[Language] = Language.FRENCH
    has_valid_driving_license: bool = False
    driver_license_number: Optional[str] = None
    driver_licence_type: Optional[List[DriverLicenceType]] = None
    last_license_check_date: Optional[date] = None
    vehicle_types: Optional[List[VehicleType]] = None
    warehouse_certifications: Optional[List[WarehouseCertification]] = None
    notifications_email: bool = True
    notifications_sms: bool = False
    notifications_push: bool = True
    is_active: bool = True
    notes: Optional[str] = None
    tags: Optional[List[UUID]] = None
    
    @field_validator('department', mode='before')
    @classmethod
    def convert_empty_department(cls, v):
        """Convert empty string to None for department."""
        if v == '':
            return None
        return v


class DriverPickerCreate(DriverPickerBase):
    """Model for creating a driver/picker."""
    password: str
    confirm_password: str


class DriverPickerUpdate(MapFlowBaseModel):
    """Model for updating a driver/picker."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    department: Optional[Department] = None
    employee_id: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[Language] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None
    has_valid_driving_license: Optional[bool] = None
    driver_license_number: Optional[str] = None
    driver_licence_type: Optional[List[DriverLicenceType]] = None
    last_license_check_date: Optional[date] = None
    vehicle_types: Optional[List[VehicleType]] = None
    warehouse_certifications: Optional[List[WarehouseCertification]] = None
    notifications_email: Optional[bool] = None
    notifications_sms: Optional[bool] = None
    notifications_push: Optional[bool] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None
    tags: Optional[List[UUID]] = None


class DriverPicker(DriverPickerBase):
    """Complete driver/picker model."""
    id: int
    organisation: Optional[UUID] = None
    organisation_name: Optional[str] = None
    full_name: Optional[str] = None
    is_verified: bool = False
    last_login: Optional[datetime] = None
    date_joined: datetime


# ============================================================================
# Vehicle Models
# ============================================================================

class VehicleBase(MapFlowBaseModel):
    """Base vehicle model."""
    name: str
    license_plate: str
    reference: Optional[str] = None
    external_id: Optional[str] = None
    external_reference: Optional[str] = None
    vehicle_type: VehicleType
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    max_weight_kg: Optional[int] = None
    max_volume_m3: Optional[Decimal] = None
    max_distance_km: Optional[int] = None
    max_items_count: Optional[int] = None
    max_speed: Optional[int] = None
    energy_type: Optional[EnergyType] = None
    consumption_per_100km: Optional[Decimal] = None
    tank_capacity: Optional[Decimal] = None
    fuel_level: Optional[Decimal] = None
    remaining_range: Optional[Decimal] = None
    status: Optional[VehicleStatus] = VehicleStatus.AVAILABLE
    required_licence_type: Optional[DriverLicenceType] = DriverLicenceType.B
    notes: Optional[str] = None
    maintenance_plan: Optional[UUID] = None
    acquisition_date: Optional[date] = None
    current_km: Optional[int] = None
    last_km_source: Optional[KmSource] = None
    technical_inspection_expiry: Optional[date] = None
    fuel_card_number: Optional[str] = None
    assigned_warehouses: Optional[List[UUID]] = None


class VehicleCreate(VehicleBase):
    """Model for creating a vehicle."""
    pass


class VehicleUpdate(VehicleBase):
    """Model for updating a vehicle."""
    pass


class Vehicle(VehicleBase):
    """Complete vehicle model."""
    id: Optional[UUID] = None
    organisation: Optional[UUID] = None
    organisation_name: Optional[str] = None
    full_name: Optional[str] = None
    is_available: bool = True
    is_operational: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @field_validator('last_km_source', mode='before')
    @classmethod
    def convert_empty_km_source(cls, v):
        """Convert empty string to None for last_km_source."""
        if v == '':
            return None
        return v


# ============================================================================
# Tag Models
# ============================================================================

class TagBase(MapFlowBaseModel):
    """Base tag model."""
    name: str
    color: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    description: Optional[str] = None


class TagCreate(TagBase):
    """Model for creating a tag."""
    pass


class TagUpdate(TagBase):
    """Model for updating a tag."""
    pass


class Tag(TagBase):
    """Complete tag model."""
    id: UUID
    usage_count: Optional[int] = None
    created_at: datetime
    updated_at: datetime


# ============================================================================
# Visit Models
# ============================================================================

class VisitBase(MapFlowBaseModel):
    """Base visit model."""
    delivery_location: UUID = Field(alias='location')
    visit_type: VisitType
    reference: Optional[str] = None
    external_id: Optional[str] = None
    external_reference: Optional[str] = None
    visit_date: Optional[date] = None
    planned_arrival_time: Optional[datetime] = None
    planned_departure_time: Optional[datetime] = None
    actual_arrival_time: Optional[datetime] = None
    actual_departure_time: Optional[datetime] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[str] = None
    driver: Optional[int] = None
    vehicle: Optional[UUID] = None
    notes: Optional[str] = None
    delivery_notes: Optional[str] = None
    customer_signature: Optional[str] = None
    driver_signature: Optional[str] = None
    is_completed: bool = False
    tags: Optional[List[UUID]] = None
    
    @field_validator('tags', mode='before')
    @classmethod
    def extract_tag_ids(cls, v):
        """Extrait les IDs des tags si l'API retourne des objets complets."""
        if v is None:
            return None
        if isinstance(v, list):
            result = []
            for tag in v:
                if isinstance(tag, UUID):
                    result.append(tag)
                elif isinstance(tag, str):
                    result.append(UUID(tag))
                elif isinstance(tag, dict) and 'id' in tag:
                    # Si c'est un objet Tag complet, extraire l'ID
                    result.append(UUID(tag['id']) if isinstance(tag['id'], str) else tag['id'])
                else:
                    result.append(tag)
            return result
        return v
    
    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class VisitCreate(VisitBase):
    """Model for creating a visit."""
    pass


class VisitUpdate(VisitBase):
    """Model for updating a visit."""
    pass


class Visit(VisitBase):
    """Complete visit model."""
    id: UUID
    organisation: Optional[UUID] = None
    customer: Optional[UUID] = None
    customer_name: Optional[str] = None
    location_name: Optional[str] = None
    full_address: Optional[str] = None
    duration_minutes: Optional[int] = None
    created_at: datetime
    updated_at: datetime


# ============================================================================
# Visit Product Models
# ============================================================================

class VisitProductBase(MapFlowBaseModel):
    """Base visit product model."""
    visit: UUID
    product: UUID
    quantity: int = Field(..., ge=0)


class VisitProductCreate(VisitProductBase):
    """Model for creating a visit product."""
    pass


class VisitProductUpdate(MapFlowBaseModel):
    """Model for updating a visit product."""
    quantity: int = Field(..., ge=0)


class VisitProduct(VisitProductBase):
    """Complete visit product model."""
    id: UUID
    visit_details: Optional[Dict[str, Any]] = None
    product_details: Optional[Dict[str, Any]] = None
    visit_reference: Optional[str] = None
    visit_date: Optional[date] = None
    visit_type_display: Optional[str] = None
    product_name: Optional[str] = None
    product_reference: Optional[str] = None
    product_type: Optional[str] = None
    unit_weight_kg: Optional[Union[str, Decimal]] = None
    unit_volume_m3: Optional[Union[str, Decimal]] = None
    total_weight_kg: Optional[Union[float, Decimal]] = None
    total_volume_m3: Optional[Union[float, Decimal]] = None
    selling_price: Optional[Union[float, Decimal]] = None
    effective_selling_price: Optional[Union[float, Decimal]] = None
    effective_selling_price_without_taxes: Optional[Union[float, Decimal]] = None
    effective_selling_price_all_taxes_included: Optional[Union[float, Decimal]] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


# ============================================================================
# Pagination Models
# ============================================================================

T = TypeVar('T')

class PaginatedResponse(MapFlowBaseModel, Generic[T]):
    """
    Generic paginated response model with typed results.
    
    Args:
        T: Type of items in the results list (e.g., Tag, Customer, Visit)
    
    Example:
        >>> response: PaginatedResponse[Tag] = client.list_tags()
        >>> tag = response.results[0]  # tag is a Tag object, not a dict
        >>> tag.id  # Autocomplétion IDE fonctionne
    """
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[T]
    # Champs optionnels pour certaines APIs (ex: tags avec pagination)
    total_pages: Optional[int] = None
    current_page: Optional[int] = None
    page_size: Optional[int] = None
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any], result_type: type) -> 'PaginatedResponse':
        """
        Crée une PaginatedResponse en convertissant les résultats au bon type.
        
        Les dictionnaires retournés par l'API sont automatiquement convertis
        en objets Pydantic typés pour une meilleure validation et autocomplétion.
        
        Args:
            data: Données brutes de l'API (dict avec 'count', 'next', 'previous', 'results')
            result_type: Type Pydantic pour convertir les résultats (ex: Tag, Customer, Visit)
        
        Returns:
            PaginatedResponse avec résultats typés
            
        Example:
            >>> data = {'count': 2, 'results': [{'id': '...', 'name': 'Tag1'}, ...]}
            >>> response = PaginatedResponse.from_api_response(data, Tag)
            >>> isinstance(response.results[0], Tag)  # True
        """
        if 'results' in data and data['results']:
            # Convertir chaque item en objet Pydantic s'il est encore un dict
            converted_results = []
            for item in data['results']:
                if isinstance(item, dict):
                    # Convertir le dict en objet Pydantic
                    converted_results.append(result_type(**item))
                elif isinstance(item, result_type):
                    # Déjà un objet Pydantic, le garder tel quel
                    converted_results.append(item)
                else:
                    # Cas rare : item déjà dans un autre format, le garder tel quel
                    converted_results.append(item)
            data = {**data, 'results': converted_results}
        
        return cls(**data)

