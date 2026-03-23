from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mapflow-co-sdk",
    version="2.0.1",
    author="MapFlow",
    author_email="support@mapflow.co",
    description="Python SDK for MapFlow route optimization API - v2 with hierarchical product support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mapflow-co/python-sdk",
    project_urls={
        "Homepage": "https://mapflow.co",
        "Documentation": "https://mapflow.readme.io/reference",
        "Bug Tracker": "https://github.com/mapflow-co/python-sdk/issues",
        "Source Code": "https://github.com/mapflow-co/python-sdk",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "pydantic>=2.0.0",
    ],
    keywords="mapflow route optimization logistics delivery api sdk tour planning fleet management python",
)

