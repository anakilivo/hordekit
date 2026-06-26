# Installation

## Requirements

- Python 3.9 or higher
- pip or uv package manager

## Installation Methods

### Using pip

The library can be installed using pip with the standard installation command.

### Using uv (Recommended)

The library can be installed using uv, which provides faster dependency resolution and better package management.

### From Source

If you want to install from the latest development version, you can clone the repository and install it directly from the source code.

## Development Installation

For development and contributing, you can install the library with all development dependencies.

This will install all development dependencies including:

- Testing tools (pytest, faker)
- Code quality tools (black, isort, flake8, mypy)
- Security tools (bandit, safety)
- Documentation tools (mkdocs)

## Verification

To verify the installation, you can import the library and test basic functionality to ensure everything is working correctly.

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure you're using Python 3.9+
2. **Permission Error**: Use `pip install --user` or a virtual environment
3. **uv not found**: Install uv first: `pip install uv`

### Virtual Environment

We recommend using a virtual environment for development to avoid conflicts with system packages. 