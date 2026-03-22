"""
Exemples d'utilisation des conteneurs et contenus (SDK v2).

Ce fichier démontre comment utiliser la gestion des conteneurs:
- Création de conteneurs (palettes, colis)
- Ajout de produits avec quantités
- Navigation dans les contenus
- Cas d'usage e-commerce: produits dans colis

Prérequis:
    pip install mapflow-co-sdk>=2.0.0

Configuration:
    export MAPFLOW_API_KEY="votre_api_key"
    # ou
    export MAPFLOW_API_URL="https://api.mapflow.co"  # optionnel
"""

import os
from mapflow import MapFlowClient
from mapflow.constants import ItemType, WeightUnit

# ============================================================================
# CONFIGURATION
# ============================================================================

API_KEY = os.getenv("MAPFLOW_API_KEY", "votre_api_key_ici")
BASE_URL = os.getenv("MAPFLOW_API_URL", "https://api.mapflow.co")

# Initialisation du client
client = MapFlowClient(api_key=API_KEY, base_url=BASE_URL, verbose=True)


def exemple_1_creer_produits_et_colis():
    """
    Exemple 1: Créer des produits et les emballer dans des colis
    
    Cas d'usage e-commerce:
    - Un commerçant a vendu 5 produits
    - Sa plateforme lui dit de les emballer dans 2 colis
    - Il crée les produits puis les ajoute aux colis avec quantités
    - Les colis (pas les produits) seront associés aux visites
    """
    print("\n" + "=" * 60)
    print("EXEMPLE 1: Produits emballés dans des colis")
    print("=" * 60)
    
    # 1. Créer les produits du catalogue
    produits = []
    
    produit1 = client.create_delivery_item({
        "reference": "PROD-LAPTOP-001",
        "name": "MacBook Pro 16\"",
        "item_type": ItemType.PRODUCT,
        "weight": 2.1,
        "weight_unit": WeightUnit.KG,
        "selling_price": 2499.00,
        "is_fragile": True
    })
    produits.append(produit1)
    print(f"✓ Produit créé: {produit1.name}")
    
    produit2 = client.create_delivery_item({
        "reference": "PROD-PHONE-001",
        "name": "iPhone 15 Pro",
        "item_type": ItemType.PRODUCT,
        "weight": 0.221,
        "weight_unit": WeightUnit.KG,
        "selling_price": 1199.00
    })
    produits.append(produit2)
    print(f"✓ Produit créé: {produit2.name}")
    
    produit3 = client.create_delivery_item({
        "reference": "PROD-WATCH-001",
        "name": "Apple Watch Ultra",
        "item_type": ItemType.PRODUCT,
        "weight": 0.061,
        "weight_unit": WeightUnit.KG,
        "selling_price": 899.00
    })
    produits.append(produit3)
    print(f"✓ Produit créé: {produit3.name}")
    
    # 2. Créer les 2 colis
    colis1 = client.create_delivery_item({
        "reference": "COLIS-001",
        "name": "Colis Informatique",
        "item_type": ItemType.PACKAGE,
        "weight": 0.5,  # Poids du colis vide
        "weight_unit": WeightUnit.KG
    })
    print(f"\n✓ Colis créé: {colis1.name}")
    print(f"  - is_container: {colis1.is_container}")
    print(f"  - is_root: {colis1.is_root}")
    
    colis2 = client.create_delivery_item({
        "reference": "COLIS-002",
        "name": "Colis Accessoires",
        "item_type": ItemType.PACKAGE,
        "weight": 0.3,
        "weight_unit": WeightUnit.KG
    })
    print(f"✓ Colis créé: {colis2.name}")
    
    # 3. Remplir le colis 1 avec laptop + phone (quantité 2)
    client.set_container_contents(
        container_id=colis1.id,
        contents=[
            {
                "item": str(produit1.id),  # MacBook
                "quantity": 1,
                "position": 1,
                "notes": "Placer en premier - FRAGILE"
            },
            {
                "item": str(produit2.id),  # iPhone x2
                "quantity": 2,
                "position": 2
            }
        ]
    )
    print(f"\n✓ Colis 1 rempli: 1x MacBook + 2x iPhone")
    
    # 4. Remplir le colis 2 avec les montres
    client.set_container_contents(
        container_id=colis2.id,
        contents=[
            {
                "item": str(produit3.id),  # Apple Watch x2
                "quantity": 2,
                "position": 1
            }
        ]
    )
    print(f"✓ Colis 2 rempli: 2x Apple Watch")
    
    # 5. Vérifier les contenus
    contents1 = client.get_container_contents(colis1.id)
    print(f"\n📦 Contenu de '{contents1['container_name']}':")
    print(f"   - {contents1['contents_count']} type(s) de produit")
    print(f"   - {contents1['total_items_quantity']} article(s) total")
    print(f"   - Poids total: {contents1['total_weight_kg']} kg")
    
    for content in contents1['contents']:
        print(f"   → {content['quantity']}x {content['item_name']}")
    
    contents2 = client.get_container_contents(colis2.id)
    print(f"\n📦 Contenu de '{contents2['container_name']}':")
    print(f"   - {contents2['total_items_quantity']} article(s)")
    print(f"   - Poids total: {contents2['total_weight_kg']} kg")
    
    return colis1.id, colis2.id, [p.id for p in produits]


def exemple_2_lister_elements_racines():
    """
    Exemple 2: Lister uniquement les éléments racines (non contenus)
    
    Les éléments racines sont les conteneurs et produits qui ne sont
    pas dans un autre conteneur. Ce sont eux qui seront livrés.
    """
    print("\n" + "=" * 60)
    print("EXEMPLE 2: Lister les éléments racines")
    print("=" * 60)
    
    racines = client.list_root_delivery_items(page_size=10)
    
    print(f"\n{racines.count} élément(s) racine(s) trouvé(s)")
    for item in racines.results[:5]:
        item_dict = item if isinstance(item, dict) else item.__dict__
        name = item_dict.get('name', 'N/A')
        item_type = item_dict.get('item_type', 'N/A')
        contents_count = item_dict.get('contents_count', 0)
        print(f"  - {name} ({item_type})")
        if contents_count > 0:
            print(f"    └─ contient {contents_count} type(s) de produit")


def exemple_3_obtenir_hierarchie_complete(colis_id):
    """
    Exemple 3: Obtenir la hiérarchie complète d'un conteneur
    """
    print("\n" + "=" * 60)
    print("EXEMPLE 3: Obtenir la hiérarchie complète")
    print("=" * 60)
    
    hierarchy = client.get_delivery_item_hierarchy(colis_id)
    
    print(f"\n📦 {hierarchy.name}")
    print(f"   - Type: {hierarchy.item_type}")
    print(f"   - Poids propre: {hierarchy.weight_kg} kg")
    print(f"   - Poids total (avec contenus): {hierarchy.total_weight_kg} kg")
    print(f"   - Valeur totale: {hierarchy.total_selling_price} EUR")
    
    if hierarchy.contents:
        print(f"   - Contenus ({len(hierarchy.contents)} type(s)):")
        for content in hierarchy.contents:
            print(f"     └─ {content.quantity}x {content.item_name} ({content.item_type})")


def exemple_4_palette_avec_colis():
    """
    Exemple 4: Créer une palette contenant plusieurs colis
    
    Structure:
        PALLET (Palette Export)
        ├── PACKAGE (Colis 1) x2
        │   └── PRODUCT (MacBook) x5
        └── PACKAGE (Colis 2) x3
            └── PRODUCT (iPhone) x10
    """
    print("\n" + "=" * 60)
    print("EXEMPLE 4: Palette contenant des colis")
    print("=" * 60)
    
    # 1. Créer la palette
    palette = client.create_delivery_item({
        "reference": "PAL-EXPORT-001",
        "name": "Palette Export Europe",
        "item_type": ItemType.PALLET,
        "weight": 25,
        "weight_unit": WeightUnit.KG
    })
    print(f"\n✓ Palette créée: {palette.name}")
    
    # 2. Créer les produits du catalogue
    laptop = client.create_delivery_item({
        "reference": "CAT-LAPTOP",
        "name": "MacBook Pro",
        "item_type": ItemType.PRODUCT,
        "weight": 2.1,
        "weight_unit": WeightUnit.KG,
        "selling_price": 2499.00
    })
    
    phone = client.create_delivery_item({
        "reference": "CAT-PHONE",
        "name": "iPhone 15",
        "item_type": ItemType.PRODUCT,
        "weight": 0.221,
        "weight_unit": WeightUnit.KG,
        "selling_price": 1199.00
    })
    
    # 3. Créer un colis type avec des laptops
    colis_laptop = client.create_delivery_item({
        "reference": "COLIS-LAPTOP",
        "name": "Colis Laptops",
        "item_type": ItemType.PACKAGE,
        "weight": 0.5,
        "weight_unit": WeightUnit.KG
    })
    client.set_container_contents(colis_laptop.id, [
        {"item": str(laptop.id), "quantity": 5, "notes": "Fragile"}
    ])
    
    # 4. Créer un colis type avec des phones
    colis_phone = client.create_delivery_item({
        "reference": "COLIS-PHONE",
        "name": "Colis iPhones",
        "item_type": ItemType.PACKAGE,
        "weight": 0.3,
        "weight_unit": WeightUnit.KG
    })
    client.set_container_contents(colis_phone.id, [
        {"item": str(phone.id), "quantity": 10}
    ])
    
    # 5. Remplir la palette avec les colis (avec quantités)
    client.set_container_contents(
        container_id=palette.id,
        contents=[
            {
                "item": str(colis_laptop.id),
                "quantity": 2,  # 2 colis de laptops
                "position": 1,
                "notes": "En bas de la palette"
            },
            {
                "item": str(colis_phone.id),
                "quantity": 3,  # 3 colis de phones
                "position": 2,
                "notes": "Au-dessus"
            }
        ]
    )
    print(f"✓ Palette remplie avec 2 colis laptops + 3 colis phones")
    
    # 6. Afficher les totaux
    palette_details = client.get_delivery_item(palette.id)
    print(f"\n📦 Récapitulatif de la palette:")
    print(f"   - Contenus: {palette_details.contents_count} type(s) de colis")
    print(f"   - Quantité totale: {palette_details.total_items_quantity} colis")
    print(f"   - Poids total: {palette_details.total_weight_kg} kg")
    print(f"   - Valeur totale: {palette_details.total_selling_price} EUR")
    
    return palette.id


def exemple_5_modifier_contenus(colis_id):
    """
    Exemple 5: Modifier les contenus d'un colis existant
    """
    print("\n" + "=" * 60)
    print("EXEMPLE 5: Modifier les contenus")
    print("=" * 60)
    
    # 1. Afficher le contenu actuel
    contents_avant = client.get_container_contents(colis_id)
    print(f"\nContenu AVANT modification:")
    print(f"   - Quantité totale: {contents_avant['total_items_quantity']}")
    
    # 2. Créer un nouveau produit
    accessoire = client.create_delivery_item({
        "reference": "PROD-CABLE",
        "name": "Câble USB-C",
        "item_type": ItemType.PRODUCT,
        "weight": 0.05,
        "weight_unit": WeightUnit.KG,
        "selling_price": 29.00
    })
    print(f"\n✓ Nouveau produit créé: {accessoire.name}")
    
    # 3. Ajouter le produit au colis
    client.add_content_to_container(
        container_id=colis_id,
        item_id=accessoire.id,
        quantity=5,
        notes="Ajouté pour accessoiriser"
    )
    print(f"✓ Ajouté: 5x {accessoire.name}")
    
    # 4. Augmenter la quantité d'un contenu existant
    if contents_avant['contents']:
        first_content = contents_avant['contents'][0]
        client.add_content_to_container(
            container_id=colis_id,
            item_id=first_content['item_id'],
            quantity=first_content['quantity'] + 2  # +2
        )
        print(f"✓ Quantité augmentée de +2 pour: {first_content['item_name']}")
    
    # 5. Afficher le nouveau contenu
    contents_apres = client.get_container_contents(colis_id)
    print(f"\nContenu APRÈS modification:")
    print(f"   - Quantité totale: {contents_apres['total_items_quantity']}")
    print(f"   - Poids total: {contents_apres['total_weight_kg']} kg")
    
    # 6. Retirer un contenu complètement
    client.remove_content_from_container(colis_id, accessoire.id)
    print(f"\n✓ Retiré complètement: {accessoire.name}")
    
    return accessoire.id


def exemple_7_retrait_granulaire():
    """
    Exemple 7: Retrait granulaire d'un produit dans un conteneur
    
    Scénario: Une palette contient 10 laptops, on doit en retirer 6
    """
    print("\n" + "=" * 60)
    print("EXEMPLE 7: Retrait granulaire")
    print("=" * 60)
    
    # 1. Créer un produit laptop
    laptop = client.create_delivery_item({
        "reference": "PROD-LAPTOP-BULK",
        "name": "MacBook Pro 16\"",
        "item_type": ItemType.PRODUCT,
        "weight": 2.1,
        "weight_unit": WeightUnit.KG,
        "selling_price": 2499.00
    })
    print(f"\n✓ Produit créé: {laptop.name}")
    
    # 2. Créer une palette
    palette = client.create_delivery_item({
        "reference": "PAL-LAPTOP-BULK",
        "name": "Palette Laptops",
        "item_type": ItemType.PALLET,
        "weight": 25.0,
        "weight_unit": WeightUnit.KG
    })
    print(f"✓ Palette créée: {palette.name}")
    
    # 3. Ajouter 10 laptops dans la palette
    client.add_content_to_container(
        container_id=palette.id,
        item_id=laptop.id,
        quantity=10,
        notes="Stock initial"
    )
    print(f"✓ Ajouté: 10x {laptop.name}")
    
    # 4. Vérifier le contenu actuel
    contents_avant = client.get_container_contents(palette.id)
    laptop_content = next((c for c in contents_avant['contents'] 
                          if c['item_id'] == str(laptop.id)), None)
    
    if laptop_content:
        print(f"\n📦 Contenu actuel:")
        print(f"   - {laptop_content['quantity']}x {laptop_content['item_name']}")
        
        # 5. Retirer 6 laptops (retrait granulaire)
        remove_result = client.remove_content_from_container(
            container_id=palette.id,
            item_id=laptop.id,
            quantity=6
        )
        
        print(f"\n✓ Retrait granulaire effectué:")
        print(f"   - Quantité retirée: {remove_result.get('removed_quantity')}")
        print(f"   - Quantité restante: {remove_result.get('remaining_quantity')}")
        print(f"   - Complètement retiré: {remove_result.get('fully_removed')}")
        
        # 6. Vérifier le nouveau contenu
        contents_apres = client.get_container_contents(palette.id)
        laptop_content_apres = next((c for c in contents_apres['contents'] 
                                     if c['item_id'] == str(laptop.id)), None)
        
        if laptop_content_apres:
            print(f"\n📦 Contenu après retrait:")
            print(f"   - {laptop_content_apres['quantity']}x {laptop_content_apres['item_name']}")
            
            # 7. Retirer complètement les laptops restants (2 options)
            # Option A: Sans spécifier quantity (retrait complet par défaut)
            remove_complete = client.remove_content_from_container(
                container_id=palette.id,
                item_id=laptop.id
            )
            
            # Option B: Avec remove_all=True (explicite)
            # remove_complete = client.remove_content_from_container(
            #     container_id=palette.id,
            #     item_id=laptop.id,
            #     remove_all=True
            # )
            
            print(f"\n✓ Retrait complet effectué:")
            print(f"   - Quantité retirée: {remove_complete.get('removed_quantity')}")
            print(f"   - Quantité restante: {remove_complete.get('remaining_quantity')}")
            print(f"   - Complètement retiré: {remove_complete.get('fully_removed')}")
            
            # 8. Vérifier que le conteneur est vide
            contents_final = client.get_container_contents(palette.id)
            print(f"\n📦 Contenu final:")
            print(f"   - {contents_final.get('contents_count', 0)} type(s) de produit")
            print(f"   - {contents_final.get('total_items_quantity', 0)} article(s)")
    
    return palette.id, laptop.id


def exemple_6_filtres_conteneurs():
    """
    Exemple 6: Utiliser les filtres pour trouver des conteneurs
    """
    print("\n" + "=" * 60)
    print("EXEMPLE 6: Filtres conteneurs")
    print("=" * 60)
    
    # 1. Lister toutes les palettes
    palettes = client.list_delivery_items(item_type=ItemType.PALLET)
    print(f"\n📦 {palettes.count} palette(s) trouvée(s)")
    
    # 2. Lister tous les colis
    colis = client.list_delivery_items(item_type=ItemType.PACKAGE)
    print(f"📦 {colis.count} colis trouvé(s)")
    
    # 3. Lister les conteneurs avec contenus (has_contents=true)
    # Note: ce filtre dépend de l'implémentation backend
    conteneurs = client.list_delivery_items(is_container=True)
    print(f"📦 {conteneurs.count} conteneur(s) (palettes + colis)")
    
    # 4. Lister uniquement les produits
    produits = client.list_delivery_items(item_type=ItemType.PRODUCT)
    print(f"📦 {produits.count} produit(s) au catalogue")


def cleanup(ids_to_delete):
    """Nettoyer les éléments créés pendant les tests"""
    print("\n" + "=" * 60)
    print("NETTOYAGE")
    print("=" * 60)
    
    for item_id in ids_to_delete:
        try:
            client.delete_delivery_item(item_id)
            print(f"✓ Supprimé: {item_id}")
        except Exception as e:
            print(f"✗ Erreur suppression {item_id}: {e}")


def main():
    """Exécuter tous les exemples"""
    print("\n" + "#" * 60)
    print("# EXEMPLES SDK MAPFLOW v2 - CONTENEURS ET CONTENUS")
    print("#" * 60)
    
    created_ids = []
    
    try:
        # Exemple 1: Produits dans colis (cas e-commerce)
        colis1_id, colis2_id, produit_ids = exemple_1_creer_produits_et_colis()
        created_ids.extend([colis1_id, colis2_id] + produit_ids)
        
        # Exemple 2: Lister les racines
        exemple_2_lister_elements_racines()
        
        # Exemple 3: Hiérarchie complète
        exemple_3_obtenir_hierarchie_complete(colis1_id)
        
        # Exemple 4: Palette avec colis
        palette_id = exemple_4_palette_avec_colis()
        created_ids.append(palette_id)
        
        # Exemple 5: Modifier les contenus
        accessoire_id = exemple_5_modifier_contenus(colis1_id)
        created_ids.append(accessoire_id)
        
        # Exemple 6: Filtres
        exemple_6_filtres_conteneurs()
        
        # Exemple 7: Retrait granulaire
        palette_bulk_id, laptop_bulk_id = exemple_7_retrait_granulaire()
        created_ids.extend([palette_bulk_id, laptop_bulk_id])
        
        print("\n" + "=" * 60)
        print("✅ TOUS LES EXEMPLES TERMINÉS AVEC SUCCÈS!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        raise
    
    finally:
        # Nettoyage (optionnel - décommenter pour supprimer les données de test)
        # cleanup(created_ids)
        pass


if __name__ == "__main__":
    main()
