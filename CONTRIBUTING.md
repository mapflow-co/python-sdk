# Contributing to MapFlow Python SDK

Thank you for your interest in contributing to the MapFlow Python SDK!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/mapflow/sdk-python.git
cd sdk-python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package in development mode:
```bash
pip install -e .
```

## Running Tests

Run all tests:
```bash
python run_tests.py
```

Run specific test file:
```bash
python -m unittest tests.test_client
```

Run with verbose output:
```bash
python -m unittest -v tests.test_client
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all public methods and classes
- Keep functions focused and single-purpose

## Adding New Features

1. Create a new branch for your feature
2. Implement the feature with appropriate tests
3. Update documentation (README.md, docstrings)
4. Ensure all tests pass
5. Submit a pull request

## Testing with Real API

To test with the real MapFlow API:

```python
from mapflow import MapFlowClient

# Use test environment
client = MapFlowClient(
    api_key="your-test-api-key",
    base_url="https://api-test.mapflow.co"  # Test environment
)
```

## Project Structure

```
sdk-python/
├── mapflow/           # Main package
│   ├── __init__.py    # Package exports
│   ├── client.py      # MapFlowClient class
│   ├── models.py      # Pydantic models
│   ├── constants.py   # Enums and constants
│   └── exceptions.py  # Custom exceptions
├── tests/             # Unit tests
├── examples/          # Usage examples
├── setup.py           # Package setup
└── README.md          # Documentation
```

## Pull Request Guidelines

- Keep PRs focused on a single feature or fix
- Include tests for new functionality
- Update documentation as needed
- Ensure all tests pass
- Follow the existing code style

## Reporting Issues

When reporting issues, please include:

- SDK version
- Python version
- Minimal code to reproduce the issue
- Expected vs actual behavior
- Any error messages or stack traces

## Questions?

For questions or discussions, please open an issue on GitHub.

