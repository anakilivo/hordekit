# GitHub Actions Workflows

This directory contains GitHub Actions workflows for the hordekit project.

## Workflows

### CI (`ci.yml`)
Runs on every push and pull request to main/develop branches.

**Features:**
- Tests against Python 3.11, 3.12, and 3.13
- Runs linting and formatting checks (black, isort, flake8, mypy)
- Executes all tests with coverage reporting
- Uploads coverage to Codecov

**Triggers:**
- Push to main/develop branches
- Pull requests to main/develop branches

### Release (`release.yml`)
Automatically creates releases when tags are pushed.

**Features:**
- Runs tests to ensure code quality
- Builds package (wheel and source distribution)
- Creates GitHub release with assets
- Generates release notes automatically

**Triggers:**
- Push tags matching pattern `v*` (e.g., v1.0.0)

### Security (`security.yml`)
Runs security checks on code and dependencies.

**Features:**
- Bandit security linter for Python code
- Safety check for vulnerable dependencies
- Weekly scheduled runs
- Uploads security reports as artifacts

**Triggers:**
- Push to main/develop branches
- Pull requests to main/develop branches
- Weekly on Sundays (scheduled)

## Usage

### Local Development
Before pushing, run the same checks locally:
```bash
make check
```

### Creating a Release
1. Update version in `pyproject.toml`
2. Create and push a tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

### Security Checks
Security reports are available as artifacts in the GitHub Actions UI.

## Dependencies

The workflows use the following tools:
- **uv**: Fast Python package manager
- **pytest**: Testing framework
- **black**: Code formatter
- **isort**: Import sorter
- **flake8**: Linter
- **mypy**: Type checker
- **bandit**: Security linter
- **safety**: Dependency vulnerability checker
- **pytest-cov**: Coverage reporting
- **build**: Package building 