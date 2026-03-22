# 🚀 START HERE - MapFlow Python SDK

Bienvenue dans le SDK Python MapFlow!

## ⚡ Installation Rapide

```bash
pip install mapflow-co-sdk
```

## 🎯 Premier Test (30 secondes)

```python
from mapflow import MapFlowClient

# Initialiser le client avec votre clé API
client = MapFlowClient(api_key="votre-cle-api")

# Lister vos clients
customers = client.list_customers()
print(f"Vous avez {customers.count} client(s)")
```

## 📖 Documentation

| Document | Description | Temps de lecture |
|----------|-------------|------------------|
| **QUICKSTART.md** | Démarrage rapide | 5 min |
| **README.md** | Documentation complète | 15 min |
| **API_REFERENCE.md** | Référence API complète | Référence |
| **USAGE_GUIDE.md** | Patterns & bonnes pratiques | 20 min |

## 🎓 Parcours d'Apprentissage

### Étape 1: Installation (5 min)
```bash
pip install mapflow-co-sdk
python verify_installation.py
```

### Étape 2: Configuration (2 min)
1. Obtenez votre clé API sur https://app.mapflow.co/settings/api-keys
2. Testez la connexion:
```python
from mapflow import MapFlowClient
client = MapFlowClient(api_key="votre-cle")
```

### Étape 3: Premier Script (10 min)
```bash
python examples/getting_started.py
```

### Étape 4: Exemples (30 min)
- `examples/basic_usage.py` - Opérations CRUD de base
- `examples/advanced_usage.py` - Fonctionnalités avancées

### Étape 5: Intégration (variable)
- `examples/integration_example.py` - Intégration complète
- `examples/common_workflows.py` - Cas d'usage courants

## 🔥 Exemples Rapides

### Créer un Client

```python
from mapflow import MapFlowClient, CustomerType

client = MapFlowClient(api_key="votre-cle-api")

customer = client.create_customer({
    "customer_type": CustomerType.COMPANY,
    "company_name": "Ma Société",
    "email": "contact@societe.com",
    "billing_city": "Paris"
})
```

### Créer un Lieu de Livraison

```python
location = client.create_delivery_location({
    "customer": customer.id,
    "name": "Bureau Principal",
    "address": "123 rue Example",
    "zip_code": "75001",
    "city": "Paris",
    "country": "FR",
    "latitude": 48.8566,
    "longitude": 2.3522
})
```

### Ajouter un Produit au Catalogue

```python
from mapflow import ItemType

produit = client.create_delivery_item({
    "name": "Ordinateur Portable",
    "item_type": ItemType.PRODUCT,
    "weight": 2.5,
    "weight_unit": "kg",
    "is_fragile": True,
    "declared_value": 1000.0,
    "currency": "EUR"
})
```

### Créer un Entrepôt

```python
from mapflow import WarehouseType

entrepot = client.create_warehouse({
    "name": "Hub Principal",
    "code": "HUB-01",
    "warehouse_type": WarehouseType.HUB,
    "address": "100 rue Logistique",
    "zip_code": "93200",
    "city": "Saint-Denis",
    "country": "FR",
    "is_start_point": True,
    "is_end_point": True
})
```

## 🎯 Cas d'Usage Courants

### Import de Données

```python
# Importer des clients depuis votre système
for client_data in external_system.get_clients():
    customer = client.create_customer({
        "customer_type": "company",
        "company_name": client_data['name'],
        "external_id": client_data['id'],
        "billing_city": client_data['city']
    })
```

### Recherche Avancée

```python
# Trouver tous les clients actifs à Paris
paris_clients = client.list_customers(
    billing_city="Paris",
    is_active=True
)

# Trouver les produits fragiles
fragile = client.list_delivery_items(
    is_fragile=True,
    weight_min=0.5,
    weight_max=10.0
)
```

### Actions en Lot

```python
# Activer plusieurs clients d'un coup
result = client.customer_bulk_action(
    action="activate",
    customer_ids=[id1, id2, id3]
)

# Ajouter des tags en lot
result = client.vehicle_bulk_action(
    action="add_tags",
    vehicle_ids=[vehicle1, vehicle2],
    tag_ids=[tag1, tag2]
)
```

## 🛠️ Scripts Utiles

| Script | Description |
|--------|-------------|
| `verify_installation.py` | Vérifier l'installation |
| `run_tests.py` | Lancer les tests |
| `examples/getting_started.py` | Assistant de démarrage |
| `examples/demo.py` | Démo interactive |

## 📚 Ressources

### Documentation Locale
- **QUICKSTART.md** - Démarrage rapide
- **README.md** - Doc complète
- **API_REFERENCE.md** - Référence API
- **USAGE_GUIDE.md** - Guide d'utilisation
- **INDEX.md** - Index de la documentation

### En Ligne
- 📖 Documentation API: https://mapflow.readme.io/reference
- 💬 Support: support@mapflow.co
- 🐛 Issues: https://github.com/mapflow/sdk-python/issues

## ⚠️ Important

### Authentification
Toutes les requêtes nécessitent une clé API valide:
- Obtenez-la sur https://app.mapflow.co/settings/api-keys
- Utilisez l'environnement de test pour le développement
- Ne committez jamais votre clé API dans le code!

### Environnements
- **Test**: Utilisez pour le développement
- **Production**: Utilisez pour la production avec données réelles

```python
# Environnement de test
client_test = MapFlowClient(
    api_key="votre-cle-test",
    base_url="https://api-test.mapflow.co"
)

# Production
client_prod = MapFlowClient(
    api_key="votre-cle-prod",
    base_url="https://api.mapflow.co"
)
```

## 🎉 Vous êtes prêt!

Le SDK MapFlow Python est installé et prêt à l'emploi.

**Commencez maintenant:**

```bash
# Vérifier l'installation
python verify_installation.py

# Démarrage interactif
python examples/getting_started.py

# Ou lisez le guide rapide
cat QUICKSTART.md
```

## 💡 Besoin d'Aide?

1. Consultez **INDEX.md** pour trouver la bonne documentation
2. Essayez les exemples dans `examples/`
3. Lisez **USAGE_GUIDE.md** pour les bonnes pratiques
4. Contactez support@mapflow.co

---

**Version:** 1.0.0  
**Python:** >=3.8  
**License:** MIT  

**Bon développement! 🚀**
