# Changelog

All notable changes to the MapFlow Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-15

### Added
- Initial release of MapFlow Python SDK
- Complete support for all MapFlow API endpoints:
  - Customer management (CRUD operations)
  - Delivery location management
  - Warehouse management
  - Global customer API (simplified atomic creation)
  - Contact management
  - Opening hours management
  - Delivery item catalog management
  - Driver/picker management
  - Vehicle management
  - Tag management
- Pydantic models for all resources with validation
- Custom exception classes for better error handling
- Bulk action support for multiple resources
- Comprehensive type hints throughout the codebase
- Pagination support for list endpoints
- Advanced filtering and search capabilities
- Full documentation with examples
- Unit tests with >90% coverage
- Examples for basic and advanced usage

### Features
- X-API-Key authentication
- Configurable base URL and timeout
- Automatic request/response handling
- JSON serialization/deserialization
- Enum support for all API enums
- Model validation with Pydantic 2.0+

### Documentation
- Complete README with usage examples
- API reference documentation
- Contributing guidelines
- Example scripts for common use cases

[1.0.0]: https://github.com/mapflow/sdk-python/releases/tag/v1.0.0

