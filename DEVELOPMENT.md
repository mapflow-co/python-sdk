# Development Guide - MapFlow Python SDK

Guide for developers working on the MapFlow Python SDK.

## Project Structure

```
sdk-python/
├── mapflow/                 # Main package
│   ├── __init__.py          # Package exports and version
│   ├── client.py            # MapFlowClient class with all methods
│   ├── models.py            # Pydantic models for validation
│   ├── constants.py         # Enums and constants
│   └── exceptions.py        # Custom exception classes
├── tests/                   # Unit tests
│   ├── __init__.py
│   ├── test_client.py       # Client method tests
│   └── test_models.py       # Model validation tests
├── examples/                # Usage examples
│   ├── basic_usage.py       # Basic CRUD examples
│   ├── advanced_usage.py    # Advanced features
│   ├── integration_example.py
│   ├── common_workflows.py
│   ├── validation_example.py
│   ├── demo.py
│   └── getting_started.py
├── setup.py                 # Package setup
├── pyproject.toml           # Modern Python packaging
├── requirements.txt         # Dependencies
├── README.md                # Main documentation
├── API_REFERENCE.md         # Complete API reference
├── USAGE_GUIDE.md           # Usage patterns
├── QUICKSTART.md            # Quick start guide
├── CHANGELOG.md             # Version history
├── CONTRIBUTING.md          # Contribution guidelines
└── LICENSE                  # MIT License
```

## Development Setup

### 1. Clone and Install

```bash
git clone https://github.com/mapflow/sdk-python.git
cd sdk-python

# Install in editable mode with dev dependencies
pip install -e .
pip install pytest pytest-cov black flake8 mypy
```

### 2. Environment Setup

Create a `.env` file (ignored by git):

```bash
MAPFLOW_API_KEY=your-test-api-key
MAPFLOW_BASE_URL=https://api-test.mapflow.co
```

### 3. Run Tests

```bash
# Run all tests
python run_tests.py

# Run with coverage
pytest --cov=mapflow tests/

# Run specific test
python -m unittest tests.test_client.TestCustomerMethods
```

## Code Style

### Formatting with Black

```bash
# Format all code
black mapflow/ tests/ examples/

# Check formatting
black --check mapflow/ tests/ examples/
```

### Linting with Flake8

```bash
# Run flake8
flake8 mapflow/ tests/ examples/

# With specific config
flake8 --max-line-length=100 --ignore=E203,W503 mapflow/
```

### Type Checking with Mypy

```bash
# Check types
mypy mapflow/

# Strict mode
mypy --strict mapflow/
```

## Adding New Features

### 1. Add New Endpoint

To add support for a new API endpoint:

**Step 1:** Add models to `mapflow/models.py`

```python
class NewResourceBase(MapFlowBaseModel):
    """Base model for new resource."""
    name: str
    description: Optional[str] = None

class NewResourceCreate(NewResourceBase):
    """Model for creating new resource."""
    pass

class NewResource(NewResourceBase):
    """Complete new resource model."""
    id: UUID
    created_at: datetime
    updated_at: datetime
```

**Step 2:** Add methods to `mapflow/client.py`

```python
def list_new_resources(self, **params) -> PaginatedResponse:
    """List new resources."""
    data = self._request('GET', '/api/new-resources/', params=params)
    return PaginatedResponse(**data)

def create_new_resource(self, resource: Union[NewResourceCreate, Dict[str, Any]]) -> NewResource:
    """Create new resource."""
    if isinstance(resource, NewResourceCreate):
        resource = resource.model_dump(exclude_none=True)
    
    data = self._request('POST', '/api/new-resources/', json=resource)
    return NewResource(**data)
```

**Step 3:** Export in `mapflow/__init__.py`

```python
from .models import NewResource, NewResourceCreate

__all__ = [
    # ... existing exports ...
    "NewResource",
    "NewResourceCreate",
]
```

**Step 4:** Add tests in `tests/test_client.py`

```python
class TestNewResourceMethods(unittest.TestCase):
    """Test new resource methods."""
    
    def setUp(self):
        self.client = MapFlowClient(api_key="test-key")
    
    @patch('mapflow.client.requests.Session.request')
    def test_list_new_resources(self, mock_request):
        # ... test implementation ...
        pass
```

### 2. Add New Enum

Add to `mapflow/constants.py`:

```python
class NewEnum(str, Enum):
    """Description of new enum."""
    VALUE1 = "value1"
    VALUE2 = "value2"
```

Export in `mapflow/__init__.py`:

```python
from .constants import NewEnum

__all__ = [
    # ... existing exports ...
    "NewEnum",
]
```

## Testing Strategy

### Unit Tests

Test individual methods with mocked requests:

```python
@patch('mapflow.client.requests.Session.request')
def test_method(self, mock_request):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "123"}
    mock_request.return_value = mock_response
    
    result = self.client.some_method()
    
    self.assertEqual(result.id, "123")
    mock_request.assert_called_once()
```

### Integration Tests

Test with real API (test environment):

```python
# tests/integration/test_real_api.py
import os
import unittest

class TestRealAPI(unittest.TestCase):
    """Integration tests with real API."""
    
    @classmethod
    def setUpClass(cls):
        api_key = os.getenv('MAPFLOW_TEST_API_KEY')
        if not api_key:
            raise unittest.SkipTest("No test API key available")
        
        cls.client = MapFlowClient(
            api_key=api_key,
            base_url="https://api-test.mapflow.co"
        )
    
    def test_create_and_delete_customer(self):
        # Create
        customer = self.client.create_customer({...})
        self.assertIsNotNone(customer.id)
        
        # Cleanup
        self.client.delete_customer(customer.id)
```

## Release Process

### 1. Update Version

Update version in:
- `mapflow/__init__.py`
- `setup.py`
- `pyproject.toml`

### 2. Update Changelog

Add new version section to `CHANGELOG.md`:

```markdown
## [1.1.0] - 2024-02-01

### Added
- New feature X
- Support for endpoint Y

### Changed
- Improved error handling for Z

### Fixed
- Bug in method A
```

### 3. Run Tests

```bash
python run_tests.py
```

### 4. Build Package

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Build
python setup.py sdist bdist_wheel
```

### 5. Test Installation

```bash
# Test in clean environment
python -m venv test_env
source test_env/bin/activate
pip install dist/mapflow_co_sdk-1.1.0-py3-none-any.whl

# Test import
python -c "import mapflow; print(mapflow.__version__)"

deactivate
rm -rf test_env
```

### 6. Publish to PyPI

```bash
# Install twine
pip install twine

# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ mapflow-co-sdk

# If all good, upload to PyPI
twine upload dist/*
```

## Debugging

### Enable Verbose Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Now all requests will be logged
client = MapFlowClient(api_key="test-key")
```

### Inspect Requests

```python
# Access the underlying session
print(client.session.headers)

# Make raw request
response = client._request('GET', '/locations/customers/')
print(response)
```

### Debug Pydantic Validation

```python
from pydantic import ValidationError

try:
    customer = CustomerCreate(invalid_field="value")
except ValidationError as e:
    print(e.json(indent=2))
```

## Performance Optimization

### 1. Connection Pooling

The SDK uses `requests.Session` which pools connections automatically.

### 2. Batch Operations

Always prefer bulk operations:

```python
# Slow
for item_id in item_ids:
    client.delete_delivery_item(item_id)

# Fast
client.delivery_item_bulk_action(
    action="delete",
    delivery_item_ids=item_ids
)
```

### 3. Efficient Pagination

```python
# Don't load all pages if not needed
def find_customer_by_email(email):
    page = 1
    while page < 100:  # Safety limit
        response = client.list_customers(search=email, page=page)
        
        for customer in response.results:
            if customer.email == email:
                return customer
        
        if not response.next:
            break
        page += 1
    
    return None
```

## Maintenance

### Updating from OpenAPI Spec

When the API is updated:

1. Get new OpenAPI spec
2. Review changes to endpoints and schemas
3. Update models in `models.py`
4. Update methods in `client.py`
5. Update enums in `constants.py`
6. Add tests for new features
7. Update documentation
8. Bump version

### Backward Compatibility

- Don't remove public methods
- Don't change method signatures
- Add new optional parameters at the end
- Deprecate before removing
- Document breaking changes in CHANGELOG

## Documentation

### Docstring Format

Use Google-style docstrings:

```python
def method_name(self, param1: str, param2: int = 10) -> ReturnType:
    """
    Short description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2. Defaults to 10.
    
    Returns:
        Description of return value
    
    Raises:
        NotFoundError: When resource is not found
        ValidationError: When data is invalid
    
    Example:
        >>> result = client.method_name("value", 20)
        >>> print(result)
    """
    pass
```

### Updating Documentation

When adding features:

1. Update method docstrings
2. Update README.md with examples
3. Update API_REFERENCE.md with details
4. Add examples to examples/ directory
5. Update CHANGELOG.md

## Useful Commands

```bash
# Install in editable mode
pip install -e .

# Run tests with coverage
pytest --cov=mapflow --cov-report=html tests/

# Format code
black mapflow/ tests/ examples/

# Type check
mypy mapflow/

# Lint
flake8 mapflow/ tests/

# Build documentation (if using Sphinx)
cd docs && make html

# Clean build artifacts
rm -rf build/ dist/ *.egg-info __pycache__

# Create distribution
python setup.py sdist bdist_wheel
```

## Troubleshooting Development Issues

### Issue: Import errors

```bash
# Reinstall in editable mode
pip uninstall mapflow-co-sdk
pip install -e .
```

### Issue: Tests failing

```bash
# Clear cache and rerun
find . -type d -name __pycache__ -exec rm -rf {} +
python run_tests.py
```

### Issue: Type hints not working

```bash
# Ensure mypy is installed
pip install mypy
mypy mapflow/
```

## Questions?

- Open an issue on GitHub
- Contact: support@mapflow.co
- Check existing issues and pull requests

