# Installation Guide - MapFlow Python SDK

## Requirements

- Python 3.8 or higher
- pip (Python package installer)

## Installation Methods

### Method 1: From PyPI (Recommended - when published)

```bash
pip install mapflow-co-sdk
```

### Method 2: From Source (Development)

```bash
# Clone the repository
git clone https://github.com/mapflow/sdk-python.git
cd sdk-python

# Install in editable mode
pip install -e .
```

### Method 3: From Local Directory

```bash
# Navigate to the SDK directory
cd /path/to/sdk-python

# Install
pip install .
```

## Verify Installation

After installation, verify everything works:

```bash
python verify_installation.py
```

Or test the import:

```python
python3 -c "import mapflow; print('MapFlow SDK version:', mapflow.__version__)"
```

## Dependencies

The SDK automatically installs these dependencies:

- **requests** (>=2.31.0) - HTTP client library
- **pydantic** (>=2.0.0) - Data validation library

### Installing Dependencies Manually

If you need to install dependencies separately:

```bash
pip install requests>=2.31.0 pydantic>=2.0.0
```

## Virtual Environment (Recommended)

Using a virtual environment is recommended to avoid dependency conflicts:

### Using venv

```bash
# Create virtual environment
python3 -m venv mapflow-env

# Activate (Linux/macOS)
source mapflow-env/bin/activate

# Activate (Windows)
mapflow-env\Scripts\activate

# Install SDK
pip install mapflow-co-sdk

# When done
deactivate
```

### Using conda

```bash
# Create environment
conda create -n mapflow python=3.11

# Activate
conda activate mapflow

# Install SDK
pip install mapflow-co-sdk

# When done
conda deactivate
```

## Troubleshooting

### Issue: "No module named 'mapflow'"

**Solution:**
```bash
# Ensure you installed the package
pip install mapflow-co-sdk

# Or if from source
pip install -e .
```

### Issue: "No module named 'requests'" or "No module named 'pydantic'"

**Solution:**
```bash
# Install dependencies
pip install requests pydantic

# Or reinstall the SDK which should install dependencies
pip install --force-reinstall mapflow-co-sdk
```

### Issue: Python version too old

**Solution:**
```bash
# Check Python version
python --version

# SDK requires Python 3.8+
# Install Python 3.8 or higher from python.org
```

### Issue: Permission denied

**Solution:**
```bash
# Install for current user only
pip install --user mapflow-co-sdk

# Or use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install mapflow-co-sdk
```

### Issue: SSL Certificate Error

**Solution:**
```bash
# Update certificates
pip install --upgrade certifi

# Or install with --trusted-host (not recommended for production)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org mapflow-co-sdk
```

## Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade mapflow-co-sdk
```

To install a specific version:

```bash
pip install mapflow-co-sdk==1.0.0
```

## Uninstalling

To remove the SDK:

```bash
pip uninstall mapflow-co-sdk
```

## Platform-Specific Notes

### macOS

```bash
# Use Python 3
python3 -m pip install mapflow-co-sdk
```

### Linux

```bash
# May need to install pip first
sudo apt-get install python3-pip

# Then install SDK
pip3 install mapflow-co-sdk
```

### Windows

```bash
# Use Python launcher
py -m pip install mapflow-co-sdk
```

## Development Installation

For contributors and developers:

```bash
# Clone repository
git clone https://github.com/mapflow/sdk-python.git
cd sdk-python

# Install in editable mode with dev dependencies
pip install -e .
pip install pytest pytest-cov black flake8 mypy

# Run tests
python run_tests.py

# Verify
python verify_installation.py
```

## Docker Installation

If using Docker:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install SDK
RUN pip install mapflow-co-sdk

# Copy your application
COPY . .

CMD ["python", "your_app.py"]
```

## Checking Installation

After installation, verify these imports work:

```python
from mapflow import (
    MapFlowClient,
    CustomerType,
    ItemType,
    VehicleType,
    MapFlowError
)

# Create client
client = MapFlowClient(api_key="your-key")

print("✓ MapFlow SDK installed successfully!")
```

## Next Steps

After successful installation:

1. **Get your API key** from https://app.mapflow.co/settings/api-keys
2. **Read the Quick Start:** [QUICKSTART.md](QUICKSTART.md)
3. **Run examples:** `python examples/getting_started.py`
4. **Read full docs:** [README.md](README.md)

## Support

If you encounter issues:

1. Check this troubleshooting section
2. Run `python verify_installation.py`
3. Check [GitHub Issues](https://github.com/mapflow/sdk-python/issues)
4. Contact support@mapflow.co

## System Requirements Summary

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| Python | 3.8 | 3.11+ |
| RAM | 256 MB | 512 MB |
| Disk | 10 MB | 50 MB |
| Network | HTTPS access | HTTPS access |

## Installation Complete! 🎉

You're ready to start using the MapFlow SDK!

```python
from mapflow import MapFlowClient

client = MapFlowClient(api_key="your-api-key")
customers = client.list_customers()

print(f"You have {customers.count} customers")
```

