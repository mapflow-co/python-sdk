"""MapFlow API Client."""

from __future__ import annotations

from typing import Optional, Dict, Any, List, Union
from uuid import UUID
from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum
import logging
import json
import requests

from .constants import DEFAULT_BASE_URL
from .exceptions import (
    MapFlowError, AuthenticationError, NotFoundError, ValidationError,
    ForbiddenError, ServerError, RateLimitError
)
from .models import (
    Customer, CustomerCreate, CustomerUpdate,
    DeliveryLocation, DeliveryLocationCreate, DeliveryLocationUpdate,
    Warehouse, WarehouseCreate, WarehouseUpdate,
    GlobalCustomer, GlobalCustomerCreate,
    LocationContact, LocationContactCreate, LocationContactUpdate,
    LocationOpeningHours, LocationOpeningHoursCreate, LocationOpeningHoursUpdate,
    DeliveryItem, DeliveryItemCreate, DeliveryItemUpdate,
    DriverPicker, DriverPickerCreate, DriverPickerUpdate,
    Vehicle, VehicleCreate, VehicleUpdate,
    Tag, TagCreate, TagUpdate,
    Visit, VisitCreate, VisitUpdate,
    VisitProduct, VisitProductCreate, VisitProductUpdate,
    PaginatedResponse
)

# Configuration du logger pour le SDK MapFlow
logger = logging.getLogger('mapflow')
# Éviter la propagation vers le logger racine pour éviter les doublons
logger.propagate = False


class MapFlowClient:
    """
    MapFlow API Client.
    
    This client provides access to all MapFlow API endpoints for route optimization
    and logistics management.
    
    Args:
        api_key: Your MapFlow API key
        base_url: Base URL for the API (default: https://api.mapflow.co)
        timeout: Request timeout in seconds (default: 30)
        verbose: Enable verbose logging (default: False). When True, logs INFO level
                 events (requests, responses) and ERROR level for exceptions.
    
    Example:
        >>> client = MapFlowClient(api_key="your-api-key", verbose=True)
        >>> customers = client.list_customers()
        >>> customer = client.create_customer(customer_data)
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 30,
        verbose: bool = False
    ):
        """Initialize MapFlow client."""
        self.api_key = api_key
        
        # Normaliser l'URL : ajouter http:// si le schéma manque
        base_url = base_url.rstrip('/')
        if not base_url.startswith(('http://', 'https://')):
            # Si c'est localhost ou 127.0.0.1, utiliser http:// par défaut
            if 'localhost' in base_url or '127.0.0.1' in base_url:
                base_url = f'http://{base_url}'
            else:
                # Pour les autres URLs, utiliser https:// par défaut
                base_url = f'https://{base_url}'
        
        self.base_url = base_url
        self.timeout = timeout
        self.verbose = verbose
        
        # Configuration du logging si verbose est activé
        if self.verbose:
            # Configurer le logger seulement s'il n'a pas déjà de handlers
            # pour éviter les doublons si plusieurs instances sont créées
            if not logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                handler.setFormatter(formatter)
                logger.addHandler(handler)
            # Toujours définir le niveau même si le handler existe déjà
            logger.setLevel(logging.INFO)
        
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and raise appropriate exceptions."""
        try:
            data = response.json()
        except ValueError:
            data = {}
        
        # Déterminer si on doit logger les réponses détaillées
        # Pour GlobalCustomer, DeliveryLocation, Visits et VisitProducts
        log_response_body = False
        url_str = str(response.url)
        if ('/global-customers/' in url_str or 
            '/delivery-locations/' in url_str or 
            '/visits/' in url_str or 
            '/visits/products/' in url_str):
            log_response_body = True
        
        # Logger la réponse si verbose est activé
        if self.verbose:
            logger.info(f"Response {response.status_code} from {response.url}")
            if log_response_body:
                # Logger le contenu de la réponse (limité pour éviter les logs trop longs)
                if data:
                    try:
                        response_str = json.dumps(data, indent=2, ensure_ascii=False)
                        # Limiter la taille du log (premiers 2000 caractères)
                        if len(response_str) > 2000:
                            response_str = response_str[:2000] + "\n... (tronqué)"
                        logger.info(f"Response body:\n{response_str}")
                    except Exception:
                        logger.info(f"Response body (non-JSON): {str(data)[:500]}")
                else:
                    logger.info("Response body: (vide)")
        
        # Accepter 200, 201, 202 (Accepted pour actions asynchrones) et 207 (Multi-Status) comme succès
        # Le code 207 est utilisé pour les opérations en lot avec résultats partiels
        if response.status_code in [200, 201, 202, 207]:
            return data
        elif response.status_code == 204:
            return {}
        elif response.status_code == 400:
            # Construire un message d'erreur plus détaillé pour les erreurs de validation
            detail = data.get('detail', None)
            
            # Si pas de 'detail', vérifier si les erreurs sont directement dans data (format Django REST)
            if not detail and data:
                # Format Django REST Framework: {"field_name": ["error message"]}
                error_messages = []
                for field, errors in data.items():
                    if isinstance(errors, list):
                        for error in errors:
                            error_messages.append(f"{field}: {error}")
                    else:
                        error_messages.append(f"{field}: {errors}")
                if error_messages:
                    detail = '; '.join(error_messages)
            
            if not detail:
                detail = 'Validation error'
            elif isinstance(detail, list):
                # Si c'est une liste d'erreurs, les formater
                error_messages = []
                for err in detail:
                    if isinstance(err, dict):
                        loc = err.get('loc', [])
                        msg = err.get('msg', '')
                        error_type = err.get('type', '')
                        error_messages.append(f"{'.'.join(str(l) for l in loc)}: {msg} ({error_type})")
                    else:
                        error_messages.append(str(err))
                detail = '; '.join(error_messages)
            elif isinstance(detail, dict):
                detail = str(detail)
            
            message = f"Validation error: {detail}"
            if self.verbose:
                try:
                    error_response_str = json.dumps(data, indent=2, ensure_ascii=False)
                    if len(error_response_str) > 2000:
                        error_response_str = error_response_str[:2000] + "\n... (tronqué)"
                    logger.error(f"ValidationError (400): {message} - URL: {response.url}\nResponse body:\n{error_response_str}")
                except Exception:
                    logger.error(f"ValidationError (400): {message} - URL: {response.url} - Response: {data}")
            raise ValidationError(
                message=message,
                status_code=400,
                response=data
            )
        elif response.status_code == 401:
            error_msg = data.get('detail', 'Authentication failed')
            if self.verbose:
                logger.error(f"AuthenticationError (401): {error_msg} - URL: {response.url}")
            raise AuthenticationError(
                message=error_msg,
                status_code=401,
                response=data
            )
        elif response.status_code == 403:
            error_msg = data.get('detail', 'Access forbidden')
            if self.verbose:
                logger.error(f"ForbiddenError (403): {error_msg} - URL: {response.url}")
            raise ForbiddenError(
                message=error_msg,
                status_code=403,
                response=data
            )
        elif response.status_code == 404:
            error_msg = data.get('detail', 'Resource not found')
            if self.verbose:
                logger.error(f"NotFoundError (404): {error_msg} - URL: {response.url}")
            raise NotFoundError(
                message=error_msg,
                status_code=404,
                response=data
            )
        elif response.status_code == 429:
            error_msg = data.get('detail', 'Rate limit exceeded')
            if self.verbose:
                logger.error(f"RateLimitError (429): {error_msg} - URL: {response.url}")
            raise RateLimitError(
                message=error_msg,
                status_code=429,
                response=data
            )
        elif response.status_code >= 500:
            # Construire un message d'erreur plus détaillé
            detail = data.get('detail', None)
            if detail:
                if isinstance(detail, list):
                    detail = '; '.join(str(d) for d in detail)
                elif isinstance(detail, dict):
                    detail = str(detail)
                message = f"Server error ({response.status_code}): {detail}"
            elif data:
                # Si pas de 'detail' mais il y a des données, afficher les données
                message = f"Server error ({response.status_code}): {str(data)[:500]}"
            else:
                # Si pas de données JSON, afficher le texte brut de la réponse
                try:
                    text = response.text[:1000]
                    # Essayer d'extraire des informations utiles depuis le HTML si c'est une page d'erreur Django
                    if '<title>' in text and '</title>' in text:
                        import re
                        title_match = re.search(r'<title>(.*?)</title>', text, re.IGNORECASE)
                        if title_match:
                            title = title_match.group(1)
                            # Chercher des messages d'erreur dans la traceback
                            traceback_match = re.search(r'ValueError:\s*(.*?)(?:\n|</)', text, re.DOTALL)
                            if traceback_match:
                                error_msg = traceback_match.group(1).strip()[:200]
                                message = f"Server error ({response.status_code}): {title} - {error_msg}"
                            else:
                                message = f"Server error ({response.status_code}): {title}"
                        else:
                            message = f"Server error ({response.status_code}): {text[:500] if text else 'No response body'}"
                    else:
                        message = f"Server error ({response.status_code}): {text[:500] if text else 'No response body'}"
                except:
                    message = f"Server error ({response.status_code}): No details available"
            if self.verbose:
                try:
                    if data:
                        error_response_str = json.dumps(data, indent=2, ensure_ascii=False)
                        if len(error_response_str) > 2000:
                            error_response_str = error_response_str[:2000] + "\n... (tronqué)"
                        logger.error(f"ServerError ({response.status_code}): {message} - URL: {response.url}\nResponse body:\n{error_response_str}")
                    else:
                        response_text = response.text[:1000] if hasattr(response, 'text') else "(vide)"
                        logger.error(f"ServerError ({response.status_code}): {message} - URL: {response.url}\nResponse body:\n{response_text}")
                except Exception:
                    logger.error(f"ServerError ({response.status_code}): {message} - URL: {response.url} - Response: {data if data else response.text[:500]}")
            raise ServerError(
                message=message,
                status_code=response.status_code,
                response=data if data else {'raw_response': response.text[:1000] if hasattr(response, 'text') else None}
            )
        else:
            error_msg = f"Unexpected error: {response.status_code}"
            if self.verbose:
                logger.error(f"MapFlowError ({response.status_code}): {error_msg} - URL: {response.url} - Response: {data}")
            raise MapFlowError(
                message=error_msg,
                status_code=response.status_code,
                response=data
            )
    
    def _serialize_for_json(self, obj: Any) -> Any:
        """Convert UUIDs and other non-serializable objects to strings for JSON."""
        if isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, dict):
            return {k: self._serialize_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_for_json(item) for item in obj]
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, time):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, Enum):  # Gérer les enums Python
            return obj.value
        else:
            return obj
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to API."""
        # Ajouter le préfixe /api/v1 si l'endpoint ne commence pas déjà par /api/
        if not endpoint.startswith('/api/'):
            endpoint = f'/api/v1{endpoint}'
        url = f"{self.base_url}{endpoint}"
        
        # Sérialiser les données JSON pour convertir les UUIDs en chaînes
        if json is not None:
            json = self._serialize_for_json(json)
        
        # Déterminer si on doit logger les payloads détaillés
        # Pour GlobalCustomer, DeliveryLocation, Visits et VisitProducts
        log_payloads = False
        if ('/global-customers/' in endpoint or 
            '/delivery-locations/' in endpoint or 
            '/visits/' in endpoint or 
            '/visits/products/' in endpoint):
            log_payloads = True
        
        # Logger la requête si verbose est activé
        if self.verbose:
            logger.info(f"Request {method} {url}")
            if log_payloads:
                if params:
                    try:
                        params_str = json.dumps(params, indent=2, ensure_ascii=False)
                        if len(params_str) > 1000:
                            params_str = params_str[:1000] + "\n... (tronqué)"
                        logger.info(f"Query parameters:\n{params_str}")
                    except Exception:
                        logger.info(f"Query parameters: {params}")
                if json:
                    try:
                        # Masquer les mots de passe dans les logs avant sérialisation
                        json_log = json.copy() if isinstance(json, dict) else json
                        if isinstance(json_log, dict):
                            for key in ['password', 'confirm_password', 'api_key', 'secret']:
                                if key in json_log:
                                    json_log[key] = "***MASKED***"
                        json_str = json.dumps(json_log, indent=2, ensure_ascii=False, default=str)
                        # Limiter la taille du log (premiers 3000 caractères)
                        if len(json_str) > 3000:
                            json_str = json_str[:3000] + "\n... (tronqué)"
                        logger.info(f"Request payload:\n{json_str}")
                    except Exception:
                        logger.info(f"Request payload (non-serializable): {str(json)[:500]}")
                if data:
                    try:
                        data_str = json.dumps(data, indent=2, ensure_ascii=False, default=str)
                        if len(data_str) > 1000:
                            data_str = data_str[:1000] + "\n... (tronqué)"
                        logger.info(f"Request data:\n{data_str}")
                    except Exception:
                        logger.info(f"Request data: {str(data)[:500]}")
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.Timeout:
            error_msg = f"Request timeout after {self.timeout}s"
            if self.verbose:
                logger.error(f"TimeoutError: {error_msg} - URL: {url}")
            raise MapFlowError(error_msg)
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection error: {str(e)}"
            if self.verbose:
                logger.error(f"ConnectionError: {error_msg} - URL: {url}")
            raise MapFlowError(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            if self.verbose:
                logger.error(f"RequestException: {error_msg} - URL: {url}")
            raise MapFlowError(error_msg)
    
    # ========================================================================
    # Customer Methods
    # ========================================================================
    
    def list_customers(self, **params) -> PaginatedResponse[Customer]:
        """
        List all customers with optional filtering.
        
        Args:
            **params: Query parameters for filtering (customer_type, is_active, etc.)
        
        Returns:
            PaginatedResponse[Customer] with list of Customer objects (not dicts)
        """
        data = self._request('GET', '/locations/customers/', params=params)
        return PaginatedResponse.from_api_response(data, Customer)
    
    def create_customer(self, customer: Union[CustomerCreate, Dict[str, Any]]) -> Customer:
        """
        Create a new customer.
        
        Args:
            customer: Customer data (CustomerCreate model or dict)
        
        Returns:
            Created customer
        """
        if isinstance(customer, CustomerCreate):
            customer = customer.model_dump(exclude_none=True)
        
        data = self._request('POST', '/locations/customers/', json=customer)
        
        # L'API peut renvoyer une réponse incomplète sans id, created_at, updated_at
        # Si c'est le cas, essayer de récupérer l'objet complet via une recherche
        if 'id' not in data:
            # Essayer de trouver le client créé via email ou external_reference
            search_params = {}
            if data.get('email'):
                search_params['email'] = data['email']
            elif customer.get('email'):
                search_params['email'] = customer['email']
            elif data.get('external_reference'):
                search_params['external_reference'] = data['external_reference']
            elif customer.get('external_reference'):
                search_params['external_reference'] = customer['external_reference']
            
            if search_params:
                # Chercher le client créé
                results = self.list_customers(**search_params)
                if results.results and len(results.results) > 0:
                    # Prendre le premier résultat (le plus récent devrait être celui qu'on vient de créer)
                    # results.results[0] est déjà un objet Customer (grâce au typage générique)
                    return results.results[0]
        
        # Si on a un id, essayer de récupérer l'objet complet
        if 'id' in data:
            try:
                return self.get_customer(data['id'])
            except:
                pass
        
        # Sinon, créer le modèle avec les données disponibles (les champs requis seront None)
        return Customer(**data)
    
    def get_customer(self, customer_id: Union[UUID, str]) -> Customer:
        """
        Get customer by ID.
        
        Args:
            customer_id: Customer UUID
        
        Returns:
            Customer object
        """
        data = self._request('GET', f'/locations/customers/{customer_id}/')
        return Customer(**data)
    
    def update_customer(
        self,
        customer_id: Union[UUID, str],
        customer: Union[CustomerUpdate, Dict[str, Any]]
    ) -> Customer:
        """
        Update customer.
        
        Args:
            customer_id: Customer UUID
            customer: Customer data (CustomerUpdate model or dict)
        
        Returns:
            Updated customer
        """
        if isinstance(customer, CustomerUpdate):
            customer = customer.model_dump(exclude_none=True)
        
        data = self._request('PUT', f'/locations/customers/{customer_id}/', json=customer)
        return Customer(**data)
    
    def patch_customer(
        self,
        customer_id: Union[UUID, str],
        customer: Union[CustomerUpdate, Dict[str, Any]]
    ) -> Customer:
        """
        Partially update customer.
        
        Args:
            customer_id: Customer UUID
            customer: Customer data (partial)
        
        Returns:
            Updated customer
        """
        if isinstance(customer, CustomerUpdate):
            customer = customer.model_dump(exclude_none=True)
        
        data = self._request('PATCH', f'/locations/customers/{customer_id}/', json=customer)
        return Customer(**data)
    
    def delete_customer(self, customer_id: Union[UUID, str]) -> None:
        """
        Delete customer.
        
        Args:
            customer_id: Customer UUID
        """
        self._request('DELETE', f'/locations/customers/{customer_id}/')
    
    def get_customer_locations(
        self,
        customer_id: Union[UUID, str],
        **params
    ) -> List[DeliveryLocation]:
        """
        Get all delivery locations for a customer.
        
        Args:
            customer_id: Customer UUID
            **params: Optional filters (is_active, city, etc.)
        
        Returns:
            List of delivery locations
        """
        data = self._request('GET', f'/locations/customers/{customer_id}/locations/', params=params)
        return [DeliveryLocation(**loc) for loc in data.get('locations', [])]
    
    def customer_bulk_action(
        self,
        action: str,
        customer_ids: List[Union[UUID, str]],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform bulk action on customers.
        
        Args:
            action: Action to perform (activate, deactivate, add_tags, etc.)
            customer_ids: List of customer UUIDs
            **kwargs: Additional parameters depending on action
        
        Returns:
            Result of bulk action
        """
        payload = {
            'action': action,
            'customer_ids': [str(cid) for cid in customer_ids],
            **kwargs
        }
        return self._request('POST', '/locations/customers/bulk_action/', json=payload)
    
    # ========================================================================
    # Delivery Location Methods
    # ========================================================================
    
    def list_delivery_locations(self, **params) -> PaginatedResponse[DeliveryLocation]:
        """
        List all delivery locations with optional filtering.
        
        Args:
            **params: Query parameters for filtering
        
        Returns:
            PaginatedResponse[DeliveryLocation] with list of DeliveryLocation objects (not dicts)
        """
        data = self._request('GET', '/locations/delivery-locations/', params=params)
        return PaginatedResponse.from_api_response(data, DeliveryLocation)
    
    def create_delivery_location(
        self,
        location: Union[DeliveryLocationCreate, Dict[str, Any]]
    ) -> DeliveryLocation:
        """
        Create a new delivery location.
        
        Args:
            location: Location data (DeliveryLocationCreate model or dict)
        
        Returns:
            Created delivery location
        """
        if isinstance(location, DeliveryLocationCreate):
            location = location.model_dump(exclude_none=True)
        
        data = self._request('POST', '/locations/delivery-locations/', json=location)
        
        # L'API peut renvoyer une réponse incomplète sans id, created_at, updated_at
        # Si c'est le cas, essayer de récupérer l'objet complet via une recherche
        if 'id' not in data:
            # Essayer de trouver le lieu créé via reference ou name
            search_params = {}
            if data.get('reference'):
                search_params['reference'] = data['reference']
            elif location.get('reference'):
                search_params['reference'] = location['reference']
            elif data.get('name'):
                search_params['name'] = data['name']
            elif location.get('name'):
                search_params['name'] = location['name']
            
            if search_params and location.get('customer'):
                search_params['customer'] = str(location['customer'])
                # Chercher le lieu créé
                results = self.list_delivery_locations(**search_params)
                if results.results and len(results.results) > 0:
                    # Prendre le premier résultat (le plus récent devrait être celui qu'on vient de créer)
                    # results.results[0] est déjà un objet DeliveryLocation (grâce au typage générique)
                    return results.results[0]
        
        # Si on a un id, essayer de récupérer l'objet complet
        if 'id' in data:
            try:
                return self.get_delivery_location(data['id'])
            except:
                pass
        
        # Sinon, créer le modèle avec les données disponibles
        return DeliveryLocation(**data)
    
    def get_delivery_location(self, location_id: Union[UUID, str]) -> DeliveryLocation:
        """
        Get delivery location by ID.
        
        Args:
            location_id: Location UUID
        
        Returns:
            DeliveryLocation object
        """
        data = self._request('GET', f'/locations/delivery-locations/{location_id}/')
        return DeliveryLocation(**data)
    
    def update_delivery_location(
        self,
        location_id: Union[UUID, str],
        location: Union[DeliveryLocationUpdate, Dict[str, Any]]
    ) -> DeliveryLocation:
        """
        Update delivery location.
        
        Args:
            location_id: Location UUID
            location: Location data
        
        Returns:
            Updated delivery location
        """
        if isinstance(location, DeliveryLocationUpdate):
            location = location.model_dump(exclude_none=True)
        
        data = self._request('PUT', f'/locations/delivery-locations/{location_id}/', json=location)
        return DeliveryLocation(**data)
    
    def patch_delivery_location(
        self,
        location_id: Union[UUID, str],
        location: Union[DeliveryLocationUpdate, Dict[str, Any]]
    ) -> DeliveryLocation:
        """
        Partially update delivery location.
        
        Args:
            location_id: Location UUID
            location: Location data (partial)
        
        Returns:
            Updated delivery location
        """
        if isinstance(location, DeliveryLocationUpdate):
            location = location.model_dump(exclude_none=True)
        
        data = self._request('PATCH', f'/locations/delivery-locations/{location_id}/', json=location)
        return DeliveryLocation(**data)
    
    def delete_delivery_location(self, location_id: Union[UUID, str]) -> None:
        """
        Delete delivery location.
        
        Args:
            location_id: Location UUID
        """
        self._request('DELETE', f'/locations/delivery-locations/{location_id}/')
    
    def delivery_location_bulk_action(
        self,
        action: str,
        location_ids: List[Union[UUID, str]],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform bulk action on delivery locations.
        
        Args:
            action: Action to perform
            location_ids: List of location UUIDs
            **kwargs: Additional parameters
        
        Returns:
            Result of bulk action
        """
        payload = {
            'action': action,
            'location_ids': [str(lid) for lid in location_ids],
            **kwargs
        }
        return self._request('POST', '/locations/delivery-locations/bulk_action/', json=payload)
    
    # ========================================================================
    # Warehouse Methods
    # ========================================================================
    
    def list_warehouses(self, **params) -> PaginatedResponse[Warehouse]:
        """
        List all warehouses with optional filtering.
        
        Args:
            **params: Query parameters for filtering
        
        Returns:
            PaginatedResponse[Warehouse] with list of Warehouse objects (not dicts)
        """
        data = self._request('GET', '/locations/warehouses/', params=params)
        return PaginatedResponse.from_api_response(data, Warehouse)
    
    def create_warehouse(self, warehouse: Union[WarehouseCreate, Dict[str, Any]]) -> Warehouse:
        """
        Create a new warehouse.
        
        Args:
            warehouse: Warehouse data
        
        Returns:
            Created warehouse
        """
        if isinstance(warehouse, WarehouseCreate):
            warehouse = warehouse.model_dump(exclude_none=True)
        
        data = self._request('POST', '/locations/warehouses/', json=warehouse)
        
        # L'API peut renvoyer une réponse incomplète sans id, created_at, updated_at
        # Si c'est le cas, essayer de récupérer l'objet complet via une recherche
        if 'id' not in data:
            # Essayer de trouver l'entrepôt créé via code ou name
            search_params = {}
            if data.get('code'):
                search_params['code'] = data['code']
            elif warehouse.get('code'):
                search_params['code'] = warehouse['code']
            elif data.get('name'):
                search_params['name'] = data['name']
            elif warehouse.get('name'):
                search_params['name'] = warehouse['name']
            
            if search_params:
                # Chercher l'entrepôt créé
                results = self.list_warehouses(**search_params)
                if results.results and len(results.results) > 0:
                    # Prendre le premier résultat (le plus récent devrait être celui qu'on vient de créer)
                    # results.results[0] est déjà un objet Warehouse (grâce au typage générique)
                    return results.results[0]
        
        # Si on a un id, essayer de récupérer l'objet complet
        if 'id' in data:
            try:
                return self.get_warehouse(data['id'])
            except:
                pass
        
        # Sinon, créer le modèle avec les données disponibles
        return Warehouse(**data)
    
    def get_warehouse(self, warehouse_id: Union[UUID, str]) -> Warehouse:
        """
        Get warehouse by ID.
        
        Args:
            warehouse_id: Warehouse UUID
        
        Returns:
            Warehouse object
        """
        data = self._request('GET', f'/locations/warehouses/{warehouse_id}/')
        return Warehouse(**data)
    
    def update_warehouse(
        self,
        warehouse_id: Union[UUID, str],
        warehouse: Union[WarehouseUpdate, Dict[str, Any]]
    ) -> Warehouse:
        """
        Update warehouse.
        
        Args:
            warehouse_id: Warehouse UUID
            warehouse: Warehouse data
        
        Returns:
            Updated warehouse
        """
        if isinstance(warehouse, WarehouseUpdate):
            warehouse = warehouse.model_dump(exclude_none=True)
        
        data = self._request('PUT', f'/locations/warehouses/{warehouse_id}/', json=warehouse)
        return Warehouse(**data)
    
    def patch_warehouse(
        self,
        warehouse_id: Union[UUID, str],
        warehouse: Union[WarehouseUpdate, Dict[str, Any]]
    ) -> Warehouse:
        """
        Partially update warehouse.
        
        Args:
            warehouse_id: Warehouse UUID
            warehouse: Warehouse data (partial)
        
        Returns:
            Updated warehouse
        """
        if isinstance(warehouse, WarehouseUpdate):
            warehouse = warehouse.model_dump(exclude_none=True)
        
        data = self._request('PATCH', f'/locations/warehouses/{warehouse_id}/', json=warehouse)
        return Warehouse(**data)
    
    def delete_warehouse(self, warehouse_id: Union[UUID, str]) -> None:
        """
        Delete warehouse.
        
        Args:
            warehouse_id: Warehouse UUID
        """
        self._request('DELETE', f'/locations/warehouses/{warehouse_id}/')
    
    def set_default_warehouse(self, warehouse_id: Union[UUID, str]) -> Warehouse:
        """
        Set warehouse as default.
        
        Args:
            warehouse_id: Warehouse UUID
        
        Returns:
            Updated warehouse
        """
        data = self._request('POST', f'/locations/warehouses/{warehouse_id}/set_default/', json={})
        return Warehouse(**data)
    
    def warehouse_bulk_action(
        self,
        action: str,
        warehouse_ids: List[Union[UUID, str]],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform bulk action on warehouses.
        
        Args:
            action: Action to perform
            warehouse_ids: List of warehouse UUIDs
            **kwargs: Additional parameters
        
        Returns:
            Result of bulk action
        """
        payload = {
            'action': action,
            'warehouse_ids': [str(wid) for wid in warehouse_ids],
            **kwargs
        }
        return self._request('POST', '/locations/warehouses/bulk_action/', json=payload)
    
    # ========================================================================
    # Global Customer Methods
    # ========================================================================
    
    def list_global_customers(self, **params) -> PaginatedResponse[GlobalCustomer]:
        """
        List all global customers (simplified API).
        
        Args:
            **params: Query parameters for filtering
        
        Returns:
            PaginatedResponse[GlobalCustomer] with list of GlobalCustomer objects (not dicts)
        """
        data = self._request('GET', '/locations/global-customers/', params=params)
        return PaginatedResponse.from_api_response(data, GlobalCustomer)
    
    def create_global_customer(
        self,
        customer: Union[GlobalCustomerCreate, Dict[str, Any]]
    ) -> GlobalCustomer:
        """
        Create a global customer (Customer + Location + Contact + Hours).
        
        Args:
            customer: Global customer data
        
        Returns:
            Created global customer (id field contains DeliveryLocation ID, customer_id contains Customer ID)
        """
        if isinstance(customer, GlobalCustomerCreate):
            customer = customer.model_dump(exclude_none=True)
        
        data = self._request('POST', '/locations/global-customers/', json=customer)
        # L'API retourne l'ID de la DeliveryLocation dans 'id' et le customer_id dans 'customer_id'
        # Le modèle GlobalCustomer utilise maintenant 'id' pour la DeliveryLocation
        return GlobalCustomer(**data)
    
    def get_global_customer(self, customer_id: Union[UUID, str]) -> GlobalCustomer:
        """
        Get global customer by ID.
        
        Args:
            customer_id: Global customer UUID (DeliveryLocation ID)
        
        Returns:
            GlobalCustomer object
        """
        data = self._request('GET', f'/locations/global-customers/{customer_id}/')
        return GlobalCustomer(**data)
    
    def update_global_customer(
        self,
        customer_id: Union[UUID, str],
        customer: Dict[str, Any]
    ) -> GlobalCustomer:
        """
        Update global customer.
        
        Args:
            customer_id: Global customer UUID
            customer: Global customer data
        
        Returns:
            Updated global customer
        """
        data = self._request('PUT', f'/locations/global-customers/{customer_id}/', json=customer)
        return GlobalCustomer(**data)
    
    def patch_global_customer(
        self,
        customer_id: Union[UUID, str],
        customer: Dict[str, Any]
    ) -> GlobalCustomer:
        """
        Partially update global customer.
        
        Args:
            customer_id: Global customer UUID
            customer: Global customer data (partial)
        
        Returns:
            Updated global customer
        """
        data = self._request('PATCH', f'/locations/global-customers/{customer_id}/', json=customer)
        return GlobalCustomer(**data)
    
    def delete_global_customer(self, customer_id: Union[UUID, str]) -> None:
        """
        Delete global customer.
        
        Args:
            customer_id: Global customer UUID
        """
        self._request('DELETE', f'/locations/global-customers/{customer_id}/')
    
    def validate_global_customer_data(self, customer: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate global customer data without creating it.
        
        Args:
            customer: Global customer data to validate
        
        Returns:
            Validation result
        """
        return self._request('POST', '/locations/global-customers/validate_data/', json=customer)
    
    # ========================================================================
    # Contact Methods
    # ========================================================================
    
    def list_contacts(self, **params) -> PaginatedResponse[LocationContact]:
        """
        List all contacts with optional filtering.
        
        Args:
            **params: Query parameters for filtering
        
        Returns:
            PaginatedResponse[LocationContact] with list of LocationContact objects (not dicts)
        """
        data = self._request('GET', '/locations/contacts/', params=params)
        return PaginatedResponse.from_api_response(data, LocationContact)
    
    def create_contact(self, contact: Union[LocationContactCreate, Dict[str, Any]]) -> LocationContact:
        """
        Create a new contact.
        
        Args:
            contact: Contact data
        
        Returns:
            Created contact
        """
        if isinstance(contact, LocationContactCreate):
            contact = contact.model_dump(exclude_none=True)
        
        data = self._request('POST', '/locations/contacts/', json=contact)
        return LocationContact(**data)
    
    def get_contact(self, contact_id: Union[UUID, str]) -> LocationContact:
        """
        Get contact by ID.
        
        Args:
            contact_id: Contact UUID
        
        Returns:
            LocationContact object
        """
        data = self._request('GET', f'/locations/contacts/{contact_id}/')
        return LocationContact(**data)
    
    def update_contact(
        self,
        contact_id: Union[UUID, str],
        contact: Union[LocationContactUpdate, Dict[str, Any]]
    ) -> LocationContact:
        """
        Update contact.
        
        Args:
            contact_id: Contact UUID
            contact: Contact data
        
        Returns:
            Updated contact
        """
        if isinstance(contact, LocationContactUpdate):
            contact = contact.model_dump(exclude_none=True)
        
        data = self._request('PUT', f'/locations/contacts/{contact_id}/', json=contact)
        # L'API peut renvoyer une réponse incomplète, récupérer l'objet complet
        try:
            return self.get_contact(contact_id)
        except:
            return LocationContact(**data)
    
    def patch_contact(
        self,
        contact_id: Union[UUID, str],
        contact: Union[LocationContactUpdate, Dict[str, Any]]
    ) -> LocationContact:
        """
        Partially update contact.
        
        Args:
            contact_id: Contact UUID
            contact: Contact data (partial)
        
        Returns:
            Updated contact
        """
        if isinstance(contact, LocationContactUpdate):
            contact = contact.model_dump(exclude_none=True)
        
        data = self._request('PATCH', f'/locations/contacts/{contact_id}/', json=contact)
        # L'API peut renvoyer une réponse incomplète, récupérer l'objet complet
        try:
            return self.get_contact(contact_id)
        except:
            return LocationContact(**data)
    
    def delete_contact(self, contact_id: Union[UUID, str]) -> None:
        """
        Delete contact.
        
        Args:
            contact_id: Contact UUID
        """
        self._request('DELETE', f'/locations/contacts/{contact_id}/')
    
    # ========================================================================
    # Opening Hours Methods
    # ========================================================================
    
    def list_opening_hours(self, **params) -> PaginatedResponse[LocationOpeningHours]:
        """
        List all opening hours with optional filtering.
        
        Args:
            **params: Query parameters for filtering
        
        Returns:
            PaginatedResponse[LocationOpeningHours] with list of LocationOpeningHours objects (not dicts)
        """
        data = self._request('GET', '/locations/opening-hours/', params=params)
        return PaginatedResponse.from_api_response(data, LocationOpeningHours)
    
    def create_opening_hours(
        self,
        hours: Union[LocationOpeningHoursCreate, Dict[str, Any]]
    ) -> LocationOpeningHours:
        """
        Create opening hours.
        
        Args:
            hours: Opening hours data
        
        Returns:
            Created opening hours
        """
        if isinstance(hours, LocationOpeningHoursCreate):
            hours = hours.model_dump(exclude_none=True)
        
        data = self._request('POST', '/locations/opening-hours/', json=hours)
        return LocationOpeningHours(**data)
    
    def get_opening_hours(self, hours_id: Union[UUID, str]) -> LocationOpeningHours:
        """
        Get opening hours by ID.
        
        Args:
            hours_id: Opening hours UUID
        
        Returns:
            LocationOpeningHours object
        """
        data = self._request('GET', f'/locations/opening-hours/{hours_id}/')
        return LocationOpeningHours(**data)
    
    def update_opening_hours(
        self,
        hours_id: Union[UUID, str],
        hours: Union[LocationOpeningHoursUpdate, Dict[str, Any]]
    ) -> LocationOpeningHours:
        """
        Update opening hours.
        
        Args:
            hours_id: Opening hours UUID
            hours: Opening hours data
        
        Returns:
            Updated opening hours
        """
        if isinstance(hours, LocationOpeningHoursUpdate):
            hours = hours.model_dump(exclude_none=True)
        
        data = self._request('PUT', f'/locations/opening-hours/{hours_id}/', json=hours)
        # L'API peut renvoyer une réponse incomplète, récupérer l'objet complet
        try:
            return self.get_opening_hours(hours_id)
        except:
            return LocationOpeningHours(**data)
    
    def patch_opening_hours(
        self,
        hours_id: Union[UUID, str],
        hours: Union[LocationOpeningHoursUpdate, Dict[str, Any]]
    ) -> LocationOpeningHours:
        """
        Partially update opening hours.
        
        Args:
            hours_id: Opening hours UUID
            hours: Opening hours data (partial)
        
        Returns:
            Updated opening hours
        """
        if isinstance(hours, LocationOpeningHoursUpdate):
            hours = hours.model_dump(exclude_none=True)
        
        data = self._request('PATCH', f'/locations/opening-hours/{hours_id}/', json=hours)
        # L'API peut renvoyer une réponse incomplète, récupérer l'objet complet
        try:
            return self.get_opening_hours(hours_id)
        except:
            return LocationOpeningHours(**data)
    
    def delete_opening_hours(self, hours_id: Union[UUID, str]) -> None:
        """
        Delete opening hours.
        
        Args:
            hours_id: Opening hours UUID
        """
        self._request('DELETE', f'/locations/opening-hours/{hours_id}/')
    
    # ========================================================================
    # Delivery Item Methods
    # ========================================================================
    
    def list_delivery_items(self, **params) -> PaginatedResponse[DeliveryItem]:
        """
        List all delivery items with optional filtering.
        
        Args:
            **params: Query parameters for filtering
        
        Returns:
            PaginatedResponse[DeliveryItem] with list of DeliveryItem objects (not dicts)
        """
        data = self._request('GET', '/catalog/delivery-items/', params=params)
        return PaginatedResponse.from_api_response(data, DeliveryItem)
    
    def create_delivery_item(
        self,
        item: Union[DeliveryItemCreate, Dict[str, Any]]
    ) -> DeliveryItem:
        """
        Create a new delivery item.
        
        Args:
            item: Delivery item data
        
        Returns:
            Created delivery item
        """
        if isinstance(item, DeliveryItemCreate):
            item = item.model_dump(exclude_none=True)
        
        data = self._request('POST', '/catalog/delivery-items/', json=item)
        return DeliveryItem(**data)
    
    def get_delivery_item(self, item_id: Union[UUID, str]) -> DeliveryItem:
        """
        Get delivery item by ID.
        
        Args:
            item_id: Delivery item UUID
        
        Returns:
            DeliveryItem object
        """
        data = self._request('GET', f'/catalog/delivery-items/{item_id}/')
        return DeliveryItem(**data)
    
    def update_delivery_item(
        self,
        item_id: Union[UUID, str],
        item: Union[DeliveryItemUpdate, Dict[str, Any]]
    ) -> DeliveryItem:
        """
        Update delivery item.
        
        Args:
            item_id: Delivery item UUID
            item: Delivery item data
        
        Returns:
            Updated delivery item
        """
        if isinstance(item, DeliveryItemUpdate):
            item = item.model_dump(exclude_none=True)
        
        data = self._request('PUT', f'/catalog/delivery-items/{item_id}/', json=item)
        return DeliveryItem(**data)
    
    def patch_delivery_item(
        self,
        item_id: Union[UUID, str],
        item: Union[DeliveryItemUpdate, Dict[str, Any]]
    ) -> DeliveryItem:
        """
        Partially update delivery item.
        
        Args:
            item_id: Delivery item UUID
            item: Delivery item data (partial)
        
        Returns:
            Updated delivery item
        """
        if isinstance(item, DeliveryItemUpdate):
            item = item.model_dump(exclude_none=True)
        
        data = self._request('PATCH', f'/catalog/delivery-items/{item_id}/', json=item)
        return DeliveryItem(**data)
    
    def delete_delivery_item(self, item_id: Union[UUID, str]) -> None:
        """
        Delete delivery item.
        
        Args:
            item_id: Delivery item UUID
        """
        self._request('DELETE', f'/catalog/delivery-items/{item_id}/')
    
    def delivery_item_bulk_action(
        self,
        action: str,
        delivery_item_ids: List[Union[UUID, str]],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform bulk action on delivery items.
        
        Args:
            action: Action to perform
            delivery_item_ids: List of delivery item UUIDs
            **kwargs: Additional parameters
        
        Returns:
            Result of bulk action
        """
        payload = {
            'action': action,
            'delivery_item_ids': [str(iid) for iid in delivery_item_ids],
            **kwargs
        }
        return self._request('POST', '/catalog/delivery-items/bulk_actions/', json=payload)
    
    # ========================================================================
    # Container Methods (v2 - Gestion des conteneurs et contenus)
    # ========================================================================
    
    def list_root_delivery_items(self, **params) -> PaginatedResponse[DeliveryItem]:
        """
        Liste uniquement les éléments racines (non contenus dans un autre).
        
        Utile pour afficher les conteneurs de niveau supérieur (palettes,
        colis autonomes, produits non emballés, etc.).
        
        Args:
            **params: Paramètres de filtrage optionnels
        
        Returns:
            PaginatedResponse[DeliveryItem] avec liste des éléments racines (objets DeliveryItem, pas des dicts)
        """
        data = self._request('GET', '/catalog/delivery-items/roots/', params=params)
        return PaginatedResponse.from_api_response(data, DeliveryItem)
    
    def get_delivery_item_hierarchy(self, item_id: Union[UUID, str]) -> DeliveryItem:
        """
        Obtient la hiérarchie complète d'un conteneur avec tous ses contenus.
        
        Retourne l'élément avec ses contenus récursivement, utile pour visualiser
        la structure d'une palette ou d'un colis avec son contenu complet.
        
        Args:
            item_id: UUID de l'élément (PALLET ou PACKAGE)
            
        Returns:
            DeliveryItem avec contenus dans le champ 'contents'
        """
        data = self._request('GET', f'/catalog/delivery-items/{item_id}/hierarchy/')
        return DeliveryItem(**data)
    
    def get_container_contents(self, container_id: Union[UUID, str]) -> Dict[str, Any]:
        """
        Obtient les contenus d'un conteneur avec les quantités.
        
        Retourne les éléments avec leurs quantités (ex: 5x MacBook, 12x iPhone)
        et les totaux calculés automatiquement.
        
        Args:
            container_id: UUID du conteneur (PALLET ou PACKAGE)
            
        Returns:
            Dict avec:
            - 'container_id', 'container_name'
            - 'contents_count': nombre de types d'éléments différents
            - 'total_items_quantity': somme des quantités
            - 'total_weight_kg', 'total_volume_m3'
            - 'contents': liste des ContainerContent
        """
        return self._request('GET', f'/catalog/delivery-items/{container_id}/contents/')
    
    def set_container_contents(
        self,
        container_id: Union[UUID, str],
        contents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Définit le contenu complet d'un conteneur avec quantités.
        
        ATTENTION: Cette méthode REMPLACE tous les contenus existants.
        
        Args:
            container_id: UUID du conteneur (PALLET ou PACKAGE)
            contents: Liste de dicts avec:
                - 'item': UUID de l'élément
                - 'quantity': quantité (int, défaut: 1)
                - 'position': ordre de chargement (int, défaut: 0)
                - 'notes': notes optionnelles (str)
        
        Returns:
            Dict avec 'message', 'created_count' et 'contents' (liste créée)
        
        Example:
            >>> client.set_container_contents(
            ...     container_id=palette_id,
            ...     contents=[
            ...         {"item": str(laptop_id), "quantity": 5, "position": 1},
            ...         {"item": str(phone_id), "quantity": 12, "position": 2}
            ...     ]
            ... )
        """
        # Convertir les UUIDs en strings si nécessaire
        serialized_contents = []
        for content in contents:
            serialized = {}
            # Copier tous les champs et convertir les UUIDs en strings
            for key, value in content.items():
                if key == 'item':
                    # Toujours convertir en string pour s'assurer que c'est bien un UUID string
                    if isinstance(value, UUID):
                        serialized[key] = str(value)
                    elif isinstance(value, str):
                        # S'assurer que c'est bien un UUID valide (format string)
                        try:
                            UUID(value)  # Valider que c'est un UUID valide
                            serialized[key] = value
                        except (ValueError, TypeError):
                            # Si ce n'est pas un UUID valide, essayer de le convertir
                            serialized[key] = str(value)
                    else:
                        serialized[key] = str(value)
                else:
                    serialized[key] = value
            serialized_contents.append(serialized)
        
        payload = {'contents': serialized_contents}
        return self._request('POST', f'/catalog/delivery-items/{container_id}/set-contents/', json=payload)
    
    def add_content_to_container(
        self,
        container_id: Union[UUID, str],
        item_id: Union[UUID, str],
        quantity: int = 1,
        position: int = 0,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ajoute ou met à jour un élément avec quantité dans un conteneur.
        
        Si l'élément existe déjà dans le conteneur, sa quantité est mise à jour.
        Sinon, un nouveau contenu est créé.
        
        Args:
            container_id: UUID du conteneur (PALLET ou PACKAGE)
            item_id: UUID de l'élément à ajouter
            quantity: Quantité (défaut: 1, doit être >= 1)
            position: Position/ordre de chargement (défaut: 0)
            notes: Notes optionnelles (ex: "Fragile", "Placer en haut")
            
        Returns:
            Dict avec 'message' et 'content' (détails du contenu créé/mis à jour)
        """
        payload = {
            'item': str(item_id),
            'quantity': quantity,
            'position': position
        }
        if notes:
            payload['notes'] = notes
        
        return self._request('POST', f'/catalog/delivery-items/{container_id}/add-content/', json=payload)
    
    def remove_content_from_container(
        self,
        container_id: Union[UUID, str],
        item_id: Union[UUID, str],
        quantity: Optional[int] = None,
        remove_all: bool = False
    ) -> Dict[str, Any]:
        """
        Retire un élément d'un conteneur (retrait granulaire ou complet).
        
        Permet de retirer une quantité spécifique d'un élément ou de retirer
        complètement l'élément du conteneur. L'élément lui-même n'est pas supprimé.
        
        Args:
            container_id: UUID du conteneur
            item_id: UUID de l'élément à retirer
            quantity: Quantité à retirer (optionnel). Si non spécifié et remove_all=False,
                     retire complètement l'élément. Si spécifié, retire seulement cette quantité.
            remove_all: Si True, retire complètement l'élément (ignore quantity)
            
        Returns:
            Dict avec:
                - 'message': Message de confirmation
                - 'item_name': Nom de l'élément retiré
                - 'removed_quantity': Quantité retirée
                - 'remaining_quantity': Quantité restante dans le conteneur
                - 'fully_removed': True si l'élément a été complètement retiré
        
        Examples:
            # Retirer 6 laptops d'une palette qui en contient 10
            result = client.remove_content_from_container(
                container_id=palette_id,
                item_id=laptop_id,
                quantity=6
            )
            # result['remaining_quantity'] == 4
            
            # Retirer complètement un élément
            result = client.remove_content_from_container(
                container_id=palette_id,
                item_id=laptop_id
            )
            # ou explicitement:
            result = client.remove_content_from_container(
                container_id=palette_id,
                item_id=laptop_id,
                remove_all=True
            )
        """
        payload = {'item_id': str(item_id)}
        
        if remove_all:
            # Si remove_all est True, on retire complètement (pas de quantity)
            pass
        elif quantity is not None:
            # Retrait granulaire : retirer seulement la quantité spécifiée
            payload['quantity'] = quantity
        # Si quantity est None et remove_all est False, on retire complètement (comportement par défaut)
        
        return self._request('POST', f'/catalog/delivery-items/{container_id}/remove-content/', json=payload)
    
    def delete_all_delivery_items(self) -> Dict[str, Any]:
        """
        Supprime TOUS les éléments de livraison de l'organisation.
        
        ATTENTION: Cette action est irréversible et supprime définitivement
        tous les DeliveryItems de votre organisation.
        
        Returns:
            Dict avec 'message', 'deleted_count' et 'organisation_id'
        """
        return self._request('POST', '/catalog/delivery-items/delete-all/', json={})
    
    # ========================================================================
    # Driver/Picker Methods
    # ========================================================================
    
    def list_drivers_pickers(self, **params) -> PaginatedResponse[DriverPicker]:
        """
        List all drivers and pickers with optional filtering.
        
        Args:
            **params: Query parameters for filtering
        
        Returns:
            PaginatedResponse[DriverPicker] with list of DriverPicker objects (not dicts)
        """
        data = self._request('GET', '/drivers-pickers/people/', params=params)
        return PaginatedResponse.from_api_response(data, DriverPicker)
    
    def create_driver_picker(
        self,
        person: Union[DriverPickerCreate, Dict[str, Any]]
    ) -> DriverPicker:
        """
        Create a new driver or picker.
        
        Args:
            person: Driver/picker data
        
        Returns:
            Created driver/picker
        """
        if isinstance(person, DriverPickerCreate):
            person = person.model_dump(exclude_none=True)
        
        data = self._request('POST', '/drivers-pickers/people/', json=person)
        return DriverPicker(**data)
    
    def get_driver_picker(self, person_id: int) -> DriverPicker:
        """
        Get driver/picker by ID.
        
        Args:
            person_id: Driver/picker ID
        
        Returns:
            DriverPicker object
        """
        data = self._request('GET', f'/drivers-pickers/people/{person_id}/')
        return DriverPicker(**data)
    
    def update_driver_picker(
        self,
        person_id: int,
        person: Union[DriverPickerUpdate, Dict[str, Any]]
    ) -> DriverPicker:
        """
        Update driver/picker.
        
        Args:
            person_id: Driver/picker ID
            person: Driver/picker data
        
        Returns:
            Updated driver/picker
        """
        if isinstance(person, DriverPickerUpdate):
            person = person.model_dump(exclude_none=True)
        
        data = self._request('PUT', f'/drivers-pickers/people/{person_id}/', json=person)
        
        # L'API peut renvoyer une réponse incomplète sans email, id, date_joined
        # Récupérer l'objet complet après la mise à jour
        try:
            return self.get_driver_picker(person_id)
        except:
            # Si la récupération échoue, essayer de créer le modèle avec les données disponibles
            # Nettoyer les chaînes vides pour les enums
            if 'department' in data and data['department'] == '':
                data['department'] = None
            return DriverPicker(**data)
    
    def patch_driver_picker(
        self,
        person_id: int,
        person: Union[DriverPickerUpdate, Dict[str, Any]]
    ) -> DriverPicker:
        """
        Partially update driver/picker.
        
        Args:
            person_id: Driver/picker ID
            person: Driver/picker data (partial)
        
        Returns:
            Updated driver/picker
        """
        if isinstance(person, DriverPickerUpdate):
            person = person.model_dump(exclude_none=True)
        
        data = self._request('PATCH', f'/drivers-pickers/people/{person_id}/', json=person)
        
        # L'API peut renvoyer une réponse incomplète sans email, id, date_joined
        # Récupérer l'objet complet après la mise à jour
        try:
            return self.get_driver_picker(person_id)
        except:
            # Si la récupération échoue, essayer de créer le modèle avec les données disponibles
            # Nettoyer les chaînes vides pour les enums
            if 'department' in data and data['department'] == '':
                data['department'] = None
            return DriverPicker(**data)
    
    def delete_driver_picker(self, person_id: int) -> None:
        """
        Delete driver/picker.
        
        Args:
            person_id: Driver/picker ID
        """
        self._request('DELETE', f'/drivers-pickers/people/{person_id}/')
    
    def reset_driver_picker_password(self, person_id: int) -> Dict[str, Any]:
        """
        Reset driver/picker password.
        
        Args:
            person_id: Driver/picker ID
        
        Returns:
            New password information
        """
        return self._request('POST', f'/drivers-pickers/people/{person_id}/reset_password/', json={})
    
    def driver_picker_bulk_action(
        self,
        action: str,
        driver_picker_ids: List[int],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform bulk action on drivers/pickers.
        
        Args:
            action: Action to perform
            driver_picker_ids: List of driver/picker IDs
            **kwargs: Additional parameters
        
        Returns:
            Result of bulk action
        """
        payload = {
            'action': action,
            'driver_picker_ids': driver_picker_ids,
            **kwargs
        }
        return self._request('POST', '/drivers-pickers/people/bulk_action/', json=payload)
    
    # ========================================================================
    # Vehicle Methods
    # ========================================================================
    
    def list_vehicles(self, **params) -> List[Vehicle]:
        """
        List all vehicles with optional filtering.
        
        Args:
            **params: Query parameters for filtering
        
        Returns:
            List of vehicles (no pagination)
        """
        data = self._request('GET', '/vehicles/vehicles/', params=params)
        return [Vehicle(**v) for v in data]
    
    def create_vehicle(self, vehicle: Union[VehicleCreate, Dict[str, Any]]) -> Vehicle:
        """
        Create a new vehicle.
        
        Args:
            vehicle: Vehicle data
        
        Returns:
            Created vehicle
        """
        if isinstance(vehicle, VehicleCreate):
            vehicle = vehicle.model_dump(exclude_none=True)
        
        data = self._request('POST', '/vehicles/vehicles/', json=vehicle)
        
        # Nettoyer les données : convertir les chaînes vides en None pour les champs enum optionnels
        # Cela évite les erreurs de validation quand l'API renvoie des chaînes vides
        for key in ['last_km_source', 'energy_type', 'status', 'required_licence_type']:
            if key in data and data[key] == '':
                data[key] = None
        
        # Si on a un id, essayer de récupérer l'objet complet
        if 'id' in data:
            try:
                return self.get_vehicle(data['id'])
            except:
                pass
        
        # Créer le modèle avec les données nettoyées
        return Vehicle(**data)
    
    def get_vehicle(self, vehicle_id: Union[UUID, str]) -> Vehicle:
        """
        Get vehicle by ID.
        
        Args:
            vehicle_id: Vehicle UUID
        
        Returns:
            Vehicle object
        """
        data = self._request('GET', f'/vehicles/vehicles/{vehicle_id}/')
        return Vehicle(**data)
    
    def update_vehicle(
        self,
        vehicle_id: Union[UUID, str],
        vehicle: Union[VehicleUpdate, Dict[str, Any]]
    ) -> Vehicle:
        """
        Update vehicle.
        
        Args:
            vehicle_id: Vehicle UUID
            vehicle: Vehicle data
        
        Returns:
            Updated vehicle
        """
        if isinstance(vehicle, VehicleUpdate):
            vehicle = vehicle.model_dump(exclude_none=True)
        
        data = self._request('PUT', f'/vehicles/vehicles/{vehicle_id}/', json=vehicle)
        return Vehicle(**data)
    
    def patch_vehicle(
        self,
        vehicle_id: Union[UUID, str],
        vehicle: Union[VehicleUpdate, Dict[str, Any]]
    ) -> Vehicle:
        """
        Partially update vehicle.
        
        Args:
            vehicle_id: Vehicle UUID
            vehicle: Vehicle data (partial)
        
        Returns:
            Updated vehicle
        """
        if isinstance(vehicle, VehicleUpdate):
            vehicle = vehicle.model_dump(exclude_none=True)
        
        data = self._request('PATCH', f'/vehicles/vehicles/{vehicle_id}/', json=vehicle)
        return Vehicle(**data)
    
    def delete_vehicle(self, vehicle_id: Union[UUID, str]) -> None:
        """
        Delete vehicle.
        
        Args:
            vehicle_id: Vehicle UUID
        """
        self._request('DELETE', f'/vehicles/vehicles/{vehicle_id}/')
    
    def vehicle_bulk_action(
        self,
        action: str,
        vehicle_ids: List[Union[UUID, str]],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform bulk action on vehicles.
        
        Args:
            action: Action to perform
            vehicle_ids: List of vehicle UUIDs
            **kwargs: Additional parameters
        
        Returns:
            Result of bulk action
        """
        payload = {
            'action': action,
            'vehicle_ids': [str(vid) for vid in vehicle_ids],
            **kwargs
        }
        return self._request('POST', '/vehicles/vehicles/bulk_action/', json=payload)
    
    # ========================================================================
    # Tag Methods
    # ========================================================================
    
    def list_tags(self, **params) -> PaginatedResponse[Tag]:
        """
        List all tags with optional filtering.
        
        Par défaut, l'API retourne tous les tags sous forme de liste directe (sans pagination).
        Pour activer la pagination, ajoutez `paginated=True` dans les params.
        
        Args:
            **params: Query parameters for filtering. Paramètres spéciaux :
                - paginated (bool): Active la pagination (default: False)
                - page (int): Numéro de page si paginated=True (default: 1)
                - page_size (int): Nombre d'éléments par page si paginated=True (default: 20, max: 1000)
                - search (str): Recherche textuelle par nom
                - ordering (str): Tri par champ (ex: 'name', '-created_at')
                - has_usage (bool): Filtrer par utilisation
                - usage_count_min (int): Nombre minimum d'utilisations
                - usage_count_max (int): Nombre maximum d'utilisations
                - created_after (str): Créé après cette date
                - created_before (str): Créé avant cette date
        
        Returns:
            PaginatedResponse[Tag] with list of Tag objects (not dicts)
            
        Examples:
            # Récupérer tous les tags (par défaut, sans pagination)
            >>> response = client.list_tags()
            >>> all_tags = response.results  # Liste complète
            
            # Avec pagination
            >>> response = client.list_tags(paginated=True, page=1, page_size=20)
            >>> tags = response.results  # Tags de la page 1
            >>> total = response.count  # Nombre total de tags
            >>> pages = response.total_pages  # Nombre total de pages
            
            # Avec filtres
            >>> response = client.list_tags(search="2026", has_usage=True)
        """
        data = self._request('GET', '/tags/visits/', params=params)
        
        # Vérifier si la pagination est activée
        paginated = params.get('paginated', False)
        # Normaliser les valeurs booléennes (True, 'true', '1', 'yes', etc.)
        if isinstance(paginated, str):
            paginated = paginated.lower() in ('true', '1', 'yes')
        
        if paginated:
            # Mode pagination : l'API retourne un objet avec count, next, previous, results, etc.
            return PaginatedResponse.from_api_response(data, Tag)
        else:
            # Mode par défaut : l'API retourne une liste directe
            if isinstance(data, list):
                # Convertir la liste en objets Tag
                tags = [Tag(**item) if isinstance(item, dict) else item for item in data]
                # Créer une structure PaginatedResponse artificielle
                return PaginatedResponse(
                    count=len(tags),
                    next=None,
                    previous=None,
                    results=tags,
                    total_pages=None,
                    current_page=None,
                    page_size=None
                )
            else:
                # Cas de fallback : si l'API retourne un objet paginé même sans paginated=True
                return PaginatedResponse.from_api_response(data, Tag)
    
    def create_tag(self, tag: Union[TagCreate, Dict[str, Any]]) -> Tag:
        """
        Create a new tag.
        
        Args:
            tag: Tag data
        
        Returns:
            Created tag
        """
        if isinstance(tag, TagCreate):
            tag = tag.model_dump(exclude_none=True)
        
        data = self._request('POST', '/tags/visits/', json=tag)
        return Tag(**data)
    
    def get_tag(self, tag_id: Union[UUID, str]) -> Tag:
        """
        Get tag by ID.
        
        Args:
            tag_id: Tag UUID
        
        Returns:
            Tag object
        """
        data = self._request('GET', f'/tags/visits/{tag_id}/')
        return Tag(**data)
    
    def update_tag(
        self,
        tag_id: Union[UUID, str],
        tag: Union[TagUpdate, Dict[str, Any]]
    ) -> Tag:
        """
        Update tag.
        
        Args:
            tag_id: Tag UUID
            tag: Tag data
        
        Returns:
            Updated tag
        """
        if isinstance(tag, TagUpdate):
            tag = tag.model_dump(exclude_none=True)
        
        data = self._request('PUT', f'/tags/visits/{tag_id}/', json=tag)
        return Tag(**data)
    
    def patch_tag(
        self,
        tag_id: Union[UUID, str],
        tag: Union[TagUpdate, Dict[str, Any]]
    ) -> Tag:
        """
        Partially update tag.
        
        Args:
            tag_id: Tag UUID
            tag: Tag data (partial)
        
        Returns:
            Updated tag
        """
        if isinstance(tag, TagUpdate):
            tag = tag.model_dump(exclude_none=True)
        
        data = self._request('PATCH', f'/tags/visits/{tag_id}/', json=tag)
        return Tag(**data)
    
    def delete_tag(self, tag_id: Union[UUID, str]) -> None:
        """
        Delete tag.
        
        Args:
            tag_id: Tag UUID
        """
        self._request('DELETE', f'/tags/visits/{tag_id}/')
    
    def tag_bulk_action(
        self,
        action: str,
        tag_ids: List[Union[UUID, str]],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform bulk action on tags.
        
        Args:
            action: Action to perform
            tag_ids: List of tag UUIDs
            **kwargs: Additional parameters
        
        Returns:
            Result of bulk action
        """
        payload = {
            'action': action,
            'tag_ids': [str(tid) for tid in tag_ids],
            **kwargs
        }
        return self._request('POST', '/tags/visits/bulk_action/', json=payload)
    
    # ========================================================================
    # Visit Methods
    # ========================================================================
    
    def list_visits(self, **params) -> PaginatedResponse[Visit]:
        """
        List all visits with optional filtering.
        
        Args:
            **params: Query parameters for filtering (visit_type, visit_date, status, etc.)
        
        Returns:
            PaginatedResponse[Visit] with list of Visit objects (not dicts)
        """
        data = self._request('GET', '/visits/', params=params)
        return PaginatedResponse.from_api_response(data, Visit)
    
    def create_visit(self, visit: Union[VisitCreate, Dict[str, Any]]) -> Visit:
        """
        Create a new visit.
        
        Args:
            visit: Visit data (VisitCreate model or dict)
        
        Returns:
            Created visit
        """
        if isinstance(visit, VisitCreate):
            # Utiliser by_alias=True pour que 'delivery_location' soit sérialisé comme 'location'
            visit = visit.model_dump(exclude_none=True, by_alias=True)
        elif isinstance(visit, dict) and 'delivery_location' in visit:
            # Si c'est un dict avec 'delivery_location', le convertir en 'location'
            visit = visit.copy()
            visit['location'] = visit.pop('delivery_location')
        
        data = self._request('POST', '/visits/', json=visit)
        return Visit(**data)
    
    def get_visit(self, visit_id: Union[UUID, str]) -> Visit:
        """
        Get visit by ID.
        
        Args:
            visit_id: Visit UUID
        
        Returns:
            Visit object
        """
        data = self._request('GET', f'/visits/{visit_id}/')
        return Visit(**data)
    
    def update_visit(
        self,
        visit_id: Union[UUID, str],
        visit: Union[VisitUpdate, Dict[str, Any]]
    ) -> Visit:
        """
        Update visit.
        
        Args:
            visit_id: Visit UUID
            visit: Visit data
        
        Returns:
            Updated visit
        """
        if isinstance(visit, VisitUpdate):
            # Utiliser by_alias=True pour que 'delivery_location' soit sérialisé comme 'location'
            visit = visit.model_dump(exclude_none=True, by_alias=True)
        elif isinstance(visit, dict) and 'delivery_location' in visit:
            # Si c'est un dict avec 'delivery_location', le convertir en 'location'
            visit = visit.copy()
            visit['location'] = visit.pop('delivery_location')
        
        data = self._request('PUT', f'/visits/{visit_id}/', json=visit)
        return Visit(**data)
    
    def patch_visit(
        self,
        visit_id: Union[UUID, str],
        visit: Union[VisitUpdate, Dict[str, Any]]
    ) -> Visit:
        """
        Partially update visit.
        
        Args:
            visit_id: Visit UUID
            visit: Visit data (partial)
        
        Returns:
            Updated visit
        """
        if isinstance(visit, VisitUpdate):
            # Utiliser by_alias=True pour que 'delivery_location' soit sérialisé comme 'location'
            visit = visit.model_dump(exclude_none=True, by_alias=True)
        elif isinstance(visit, dict) and 'delivery_location' in visit:
            # Si c'est un dict avec 'delivery_location', le convertir en 'location'
            visit = visit.copy()
            visit['location'] = visit.pop('delivery_location')
        
        data = self._request('PATCH', f'/visits/{visit_id}/', json=visit)
        return Visit(**data)
    
    def delete_visit(self, visit_id: Union[UUID, str]) -> None:
        """
        Delete visit.
        
        Args:
            visit_id: Visit UUID
        """
        self._request('DELETE', f'/visits/{visit_id}/')
    
    def visit_bulk_action(
        self,
        action: str,
        visit_ids: List[Union[UUID, str]],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform bulk action on visits.
        
        Args:
            action: Action to perform
            visit_ids: List of visit UUIDs
            **kwargs: Additional parameters
        
        Returns:
            Result of bulk action
        """
        payload = {
            'action': action,
            'visit_ids': [str(vid) for vid in visit_ids],
            **kwargs
        }
        return self._request('POST', '/visits/bulk_action/', json=payload)
    
    # ========================================================================
    # Visit Product Methods
    # ========================================================================
    
    def list_visit_products(self, **params) -> PaginatedResponse[VisitProduct]:
        """
        List all visit products with optional filtering.
        
        Args:
            **params: Query parameters for filtering (visit, product, quantity, etc.)
        
        Returns:
            PaginatedResponse[VisitProduct] with list of VisitProduct objects (not dicts)
        """
        data = self._request('GET', '/visits/products/', params=params)
        return PaginatedResponse.from_api_response(data, VisitProduct)
    
    def create_visit_product(
        self,
        visit_product: Union[VisitProductCreate, Dict[str, Any]]
    ) -> VisitProduct:
        """
        Create a new visit product (add product to a visit).
        
        Args:
            visit_product: Visit product data (VisitProductCreate model or dict)
        
        Returns:
            Created visit product
        """
        if isinstance(visit_product, VisitProductCreate):
            visit_product = visit_product.model_dump(exclude_none=True)
        
        data = self._request('POST', '/visits/products/', json=visit_product)
        return VisitProduct(**data)
    
    def get_visit_product(self, visit_product_id: Union[UUID, str]) -> VisitProduct:
        """
        Get visit product by ID.
        
        Args:
            visit_product_id: Visit product UUID
        
        Returns:
            VisitProduct object
        """
        data = self._request('GET', f'/visits/products/{visit_product_id}/')
        return VisitProduct(**data)
    
    def update_visit_product(
        self,
        visit_product_id: Union[UUID, str],
        visit_product: Union[VisitProductUpdate, Dict[str, Any]]
    ) -> VisitProduct:
        """
        Update visit product.
        
        Args:
            visit_product_id: Visit product UUID
            visit_product: Visit product data
        
        Returns:
            Updated visit product
        """
        if isinstance(visit_product, VisitProductUpdate):
            visit_product = visit_product.model_dump(exclude_none=True)
        
        data = self._request('PUT', f'/visits/products/{visit_product_id}/', json=visit_product)
        return VisitProduct(**data)
    
    def patch_visit_product(
        self,
        visit_product_id: Union[UUID, str],
        visit_product: Union[VisitProductUpdate, Dict[str, Any]]
    ) -> VisitProduct:
        """
        Partially update visit product.
        
        Args:
            visit_product_id: Visit product UUID
            visit_product: Visit product data (partial)
        
        Returns:
            Updated visit product
        """
        if isinstance(visit_product, VisitProductUpdate):
            visit_product = visit_product.model_dump(exclude_none=True)
        
        data = self._request('PATCH', f'/visits/products/{visit_product_id}/', json=visit_product)
        return VisitProduct(**data)
    
    def delete_visit_product(self, visit_product_id: Union[UUID, str]) -> None:
        """
        Delete visit product.
        
        Args:
            visit_product_id: Visit product UUID
        """
        self._request('DELETE', f'/visits/products/{visit_product_id}/')
    
    def visit_product_bulk_action(
        self,
        action: str,
        visitproduct_ids: List[Union[UUID, str]],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform bulk action on visit products.
        
        Args:
            action: Action to perform (update_quantity, multiply_quantity)
            visitproduct_ids: List of visit product UUIDs
            **kwargs: Additional parameters (new_quantity, quantity_multiplier)
        
        Returns:
            Result of bulk action
        """
        payload = {
            'action': action,
            'visitproduct_ids': [str(vpid) for vpid in visitproduct_ids],
            **kwargs
        }
        return self._request('POST', '/visits/products/bulk_action/', json=payload)

