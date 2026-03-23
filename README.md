# MapFlow Python SDK

**Official Python SDK for [MapFlow](https://mapflow.co) — Route Optimization & Delivery Management API**  
**SDK Python officiel pour [MapFlow](https://mapflow.co) — Optimisation de Tournées & Gestion Logistique**

[![PyPI version](https://img.shields.io/pypi/v/mapflow-co-sdk.svg)](https://pypi.org/project/mapflow-co-sdk/)
[![Python](https://img.shields.io/pypi/pyversions/mapflow-co-sdk.svg)](https://pypi.org/project/mapflow-co-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![API Docs](https://img.shields.io/badge/API-docs-green.svg)](https://mapflow.readme.io/reference)

---

🇬🇧 [English](#english) · 🇫🇷 [Français](#français)

---

<a name="english"></a>
## 🇬🇧 English

[MapFlow](https://mapflow.co) is a SaaS platform for **route optimization**, **delivery planning**, and **logistics management**. This SDK gives Python developers full programmatic access to the MapFlow API — manage customers, warehouses, drivers, vehicles, delivery schedules, and hierarchical product structures directly from your applications.

→ **Website**: [https://mapflow.co](https://mapflow.co)  
→ **API Reference**: [https://mapflow.readme.io/reference](https://mapflow.readme.io/reference)  
→ **Get your API key**: [app.mapflow.co → Settings → API Keys](https://app.mapflow.co)

### Features

- **Full API coverage** — customers, locations, warehouses, drivers, vehicles, catalog, visits, and more
- **Hierarchical product structures** — pallets containing packages containing products (v2)
- **Pydantic v2 models** — type-safe request/response objects with automatic validation
- **Paginated responses** — generic `PaginatedResponse[T]` with automatic deserialization
- **Bulk operations** — activate, deactivate, update, tag multiple records in one request
- **Flexible input** — pass Pydantic models or plain dicts to any write method
- **Rich error handling** — typed exceptions with HTTP status codes and API error details
- **Verbose mode** — built-in request/response logging for debugging
- **Python 3.8+** compatible

### Installation

```bash
pip install mapflow-co-sdk
```

Install from source:

```bash
git clone https://github.com/mapflow-co/python-sdk.git
cd python-sdk
pip install -e .
```

### Quick Start

```python
from mapflow import MapFlowClient, CustomerType, VisitType, ItemType

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

### Authentication

```python
client = MapFlowClient(
    api_key="your-api-key",             # required — get it at app.mapflow.co → Settings → API Keys
    base_url="https://api.mapflow.co",  # optional — default shown
    timeout=30,                          # optional — seconds
    verbose=False                        # optional — logs requests/responses
)
```

### Core Resources

| Resource | Methods |
|----------|---------|
| **Customers** | `create/get/list/update/patch/delete_customer`, `get_customer_locations`, `customer_bulk_action` |
| **Delivery Locations** | `create/get/list/update/patch/delete_delivery_location` |
| **Global Customers** | `create_global_customer` — creates customer + location + contact + opening hours atomically |
| **Warehouses** | `create/get/list/update/patch/delete_warehouse`, `set_default_warehouse` |
| **Contacts** | `create/get/list/update/patch/delete_contact` |
| **Opening Hours** | `create/get/list/update/patch/delete_opening_hours` |
| **Product Catalog** | `create/get/list/update/patch/delete_delivery_item`, hierarchy methods |
| **Container Hierarchy** | `set_container_contents`, `get_delivery_item_hierarchy`, `add/remove_content_from_container` |
| **Drivers & Pickers** | `create/get/list/update/patch/delete_driver_picker`, `reset_driver_picker_password` |
| **Vehicles** | `create/get/list/update/patch/delete_vehicle` |
| **Visits** | `create/get/list/update/patch/delete_visit` |
| **Visit Products** | `create/get/list/update/patch/delete_visit_product`, `visit_product_bulk_action` |
| **Tags** | `create/get/list/update/patch/delete_tag` |

### Container Hierarchy (v2)

```python
from mapflow import ItemType, WeightUnit

# Create a pallet → boxes → products
pallet = client.create_delivery_item({"name": "Export Pallet", "item_type": ItemType.PALLET, "weight": 25})
box    = client.create_delivery_item({"name": "Laptop Box",    "item_type": ItemType.PACKAGE, "weight": 0.5})
laptop = client.create_delivery_item({"name": "Laptop Pro",    "item_type": ItemType.PRODUCT, "weight": 2.1, "selling_price": 2499.0})

client.set_container_contents(box.id,    [{"item": str(laptop.id), "quantity": 5}])
client.set_container_contents(pallet.id, [{"item": str(box.id),    "quantity": 3}])

hierarchy = client.get_delivery_item_hierarchy(pallet.id)
print(f"Total: {hierarchy.total_weight_kg} kg — {hierarchy.total_selling_price} EUR")
```

### Error Handling

```python
from mapflow import AuthenticationError, NotFoundError, ValidationError, RateLimitError

try:
    customer = client.get_customer(customer_id)
except AuthenticationError:
    print("Invalid API key — check app.mapflow.co → Settings → API Keys")
except NotFoundError:
    print("Customer not found")
except ValidationError as e:
    print(f"Validation error: {e.message} — {e.response}")
except RateLimitError:
    print("Rate limit exceeded — slow down requests")
```

### Pagination

```python
page = client.list_customers(page=1, page_size=20)
print(f"Total: {page.count} — Pages: {page.total_pages}")
for customer in page.results:  # typed as List[Customer]
    print(customer.display_name)
```

### Examples

```bash
export MAPFLOW_API_KEY="your-api-key"
python examples/hierarchy_example.py
python examples/visit_products_example.py
```

---

<a name="français"></a>
## 🇫🇷 Français

[MapFlow](https://mapflow.co) est une plateforme SaaS d'**optimisation de tournées**, de **planification de livraisons** et de **gestion logistique**. Ce SDK Python donne aux développeurs un accès programmatique complet à l'API MapFlow — gérez vos clients, entrepôts, chauffeurs, véhicules, tournées de livraison et catalogues produits directement depuis vos applications.

**Mots-clés** : optimisation de tournées · logiciel de planification de livraisons · gestion de flotte · logistique du dernier kilomètre · planification d'itinéraires · tournée de livraison · optimisateur de tournées · gestion logistique Python · API livraison Python · SDK logistique

→ **Site web** : [https://mapflow.co](https://mapflow.co)  
→ **Documentation API** : [https://mapflow.readme.io/reference](https://mapflow.readme.io/reference)  
→ **Obtenir votre clé API** : [app.mapflow.co → Paramètres → Clés API](https://app.mapflow.co)

### Fonctionnalités

- **Couverture complète de l'API** — clients, lieux de livraison, entrepôts, chauffeurs, véhicules, catalogue, visites
- **Structures produit hiérarchiques** — palettes contenant des colis contenant des produits (v2)
- **Modèles Pydantic v2** — objets requête/réponse typés avec validation automatique
- **Réponses paginées** — `PaginatedResponse[T]` générique avec désérialisation automatique
- **Actions en lot** — activer, désactiver, mettre à jour, taguer plusieurs enregistrements en une requête
- **Entrées flexibles** — passez des modèles Pydantic ou des dictionnaires simples
- **Gestion des erreurs enrichie** — exceptions typées avec codes HTTP et détails de l'API
- **Mode verbose** — journalisation intégrée des requêtes/réponses pour le débogage
- **Compatible Python 3.8+**

### Installation

```bash
pip install mapflow-co-sdk
```

Installation depuis les sources :

```bash
git clone https://github.com/mapflow-co/python-sdk.git
cd python-sdk
pip install -e .
```

### Démarrage rapide

```python
from mapflow import MapFlowClient, CustomerType, VisitType, ItemType

client = MapFlowClient(api_key="votre-cle-api")

# Créer un client
customer = client.create_customer({
    "customer_type": CustomerType.COMPANY,
    "company_name": "Acme Corp",
    "email": "contact@acme.com"
})

# Créer un lieu de livraison
location = client.create_delivery_location({
    "customer": str(customer.id),
    "name": "Siège Social",
    "address": "42 Rue de la Paix",
    "zip_code": "75001",
    "city": "Paris"
})

# Planifier une visite de livraison
visit = client.create_visit({
    "delivery_location": str(location.id),
    "visit_type": VisitType.DELIVERY,
    "visit_date": "2026-04-01"
})

print(f"Visite planifiée : {visit.id}")
```

### Authentification

```python
client = MapFlowClient(
    api_key="votre-cle-api",             # requis — obtenez-la sur app.mapflow.co → Paramètres → Clés API
    base_url="https://api.mapflow.co",   # optionnel — valeur par défaut
    timeout=30,                           # optionnel — en secondes
    verbose=False                         # optionnel — journalise les requêtes/réponses
)
```

### Ressources principales

| Ressource | Description |
|-----------|-------------|
| **Clients** | Gestion des clients individuels et entreprises avec adresse de facturation, SIRET, TVA |
| **Lieux de livraison** | Adresses physiques avec géolocalisation, accès poids lourds, quai de chargement |
| **Clients globaux** | Création atomique : client + lieu + contact + horaires d'ouverture en une seule requête |
| **Entrepôts** | Bases opérationnelles de la flotte — points de départ/arrivée, équipements, capacités |
| **Catalogue produits** | Produits, services, colis et palettes avec poids, volume, prix et contraintes température |
| **Hiérarchie conteneurs** | Palettes → colis → produits avec suivi des quantités et totaux calculés |
| **Chauffeurs & Préparateurs** | Gestion des chauffeurs avec types de permis, certifications CACES, types de véhicules |
| **Véhicules** | Flotte avec capacité, carburant, statut maintenance, coordonnées GPS |
| **Visites** | Tournées de livraison, enlèvements, interventions avec horaires planifiés/réels |
| **Produits de visite** | Association articles du catalogue aux visites avec quantités |
| **Tags** | Étiquettes colorées pour les visites, chauffeurs et clients |

### Hiérarchie de conteneurs (v2)

```python
from mapflow import ItemType, WeightUnit

# Créer une palette → colis → produits
palette = client.create_delivery_item({"name": "Palette Export", "item_type": ItemType.PALLET,   "weight": 25})
colis   = client.create_delivery_item({"name": "Colis Laptops",  "item_type": ItemType.PACKAGE,  "weight": 0.5})
laptop  = client.create_delivery_item({"name": "MacBook Pro",    "item_type": ItemType.PRODUCT,  "weight": 2.1, "selling_price": 2499.0})

# Remplir le colis avec 5 laptops, puis la palette avec 3 colis
client.set_container_contents(colis.id,   [{"item": str(laptop.id), "quantity": 5, "notes": "Fragile"}])
client.set_container_contents(palette.id, [{"item": str(colis.id),  "quantity": 3, "position": 1}])

# Inspecter la hiérarchie complète
hierarchy = client.get_delivery_item_hierarchy(palette.id)
print(f"Poids total : {hierarchy.total_weight_kg} kg — Valeur : {hierarchy.total_selling_price} EUR")
```

### Global Customers — création atomique

```python
global_customer = client.create_global_customer({
    "customer_type": "company",
    "company_name": "Tech Solutions SARL",
    "email": "contact@techsolutions.fr",
    "delivery_location": {
        "name": "Bureau Principal",
        "address": "10 Rue de la Tech",
        "zip_code": "69001",
        "city": "Lyon"
    },
    "contact": {
        "first_name": "Marie",
        "last_name": "Martin",
        "position": "Responsable Logistique",
        "emails": ["marie@techsolutions.fr"],
        "is_primary": True
    },
    "opening_hours": [
        {"day_of_week": 0, "opening_time": "09:00", "closing_time": "18:00"},  # Lundi
        {"day_of_week": 1, "opening_time": "09:00", "closing_time": "18:00"},  # Mardi
    ]
})
```

### Actions en lot

```python
# Activer des clients en lot
client.customer_bulk_action("activate", customer_ids=[id1, id2, id3])

# Ajouter des tags en lot
client.customer_bulk_action("add_tags", customer_ids=[id1, id2], tag_ids=[tag.id])

# Mettre à jour le statut des véhicules en lot
client.vehicle_bulk_action("change_status", vehicle_ids=[v1, v2], new_status="maintenance")

# Mettre à jour les quantités de visite en lot
client.visit_product_bulk_action("multiply_quantity", visitproduct_ids=[vp1, vp2], quantity_multiplier="2.0")
```

### Gestion des erreurs

```python
from mapflow import AuthenticationError, NotFoundError, ValidationError, RateLimitError, MapFlowError

try:
    customer = client.get_customer(customer_id)
except AuthenticationError:
    print("Clé API invalide — vérifiez sur app.mapflow.co → Paramètres → Clés API")
except NotFoundError:
    print("Client introuvable")
except ValidationError as e:
    print(f"Erreur de validation : {e.message}")
    print(f"Détails : {e.response}")
except RateLimitError:
    print("Limite de taux dépassée — ralentissez vos requêtes")
except MapFlowError as e:
    print(f"Erreur MapFlow {e.status_code} : {e.message}")
```

### Pagination

```python
page = client.list_customers(page=1, page_size=20)
print(f"Total : {page.count} — Pages : {page.total_pages}")

for customer in page.results:  # typé List[Customer]
    print(customer.display_name)

# Itérer sur toutes les pages
page_num = 1
while True:
    page = client.list_customers(page=page_num, page_size=50)
    for customer in page.results:
        traiter(customer)
    if not page.next:
        break
    page_num += 1
```

### Référence des enums

| Enum | Valeurs |
|------|---------|
| `CustomerType` | `individual`, `company` |
| `ItemType` | `PRODUCT`, `SERVICE`, `PACKAGE`, `PALLET` |
| `VisitType` | `delivery`, `pickup`, `service`, `delivery_pickup` |
| `VehicleType` | `bicycle`, `cargo_bike`, `van_small`, `van_medium`, `van_large`, `truck_small`, `truck_medium`, `truck_large`, `semi_trailer`, `refrigerated`, … |
| `VehicleStatus` | `available`, `in_use`, `maintenance`, `broken`, `retired` |
| `EnergyType` | `gasoline`, `diesel`, `electric`, `hybrid`, `hydrogen` |
| `DriverLicenceType` | `none`, `am`, `a1`, `a`, `b`, `c1`, `c`, `ce`, `d` |
| `WarehouseType` | `distribution`, `storage`, `hub`, `pickup`, `cross_dock`, `other` |
| `WeightUnit` | `kg`, `g`, `lb`, `oz`, `t` |
| `VolumeUnit` | `m3`, `l`, `ml`, `cm3`, `ft3`, `gal` |
| `DayOfWeek` | `MONDAY` (0) … `SUNDAY` (6) |

---

## Support

- **Site web / Website**: [https://mapflow.co](https://mapflow.co)
- **Documentation API**: [https://mapflow.readme.io/reference](https://mapflow.readme.io/reference)
- **Email**: support@mapflow.co
- **GitHub Issues**: [https://github.com/mapflow-co/python-sdk/issues](https://github.com/mapflow-co/python-sdk/issues)

## Licence / License

[MIT](LICENSE) © [MapFlow](https://mapflow.co)
