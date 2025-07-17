# Testing Guide for Bootstrap Ubuntu

This guide explains how to run tests for the Bootstrap Ubuntu project.

## Test Structure

The project uses multiple testing frameworks:

- **Molecule**: For testing Ansible roles in Docker containers
- **Pytest**: For testing Python code (configuration wizard)
- **Ansible-lint**: For Ansible playbook linting
- **Yamllint**: For YAML syntax validation

## Prerequisites

Install test dependencies:

```bash
pip install -r requirements-dev.txt
```

## Running Tests

### Quick Test Suite

Run linting and Python tests only:

```bash
./run_tests.sh
```

### Full Test Suite

Run all tests including Molecule (requires Docker):

```bash
./run_tests.sh --full
```

### Individual Test Types

#### Linting

```bash
# YAML linting
yamllint .

# Ansible linting
ansible-lint
```

#### Python Tests

```bash
# Run all Python tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=. --cov-report=html
```

#### Molecule Tests

```bash
# Test default scenario (all roles)
molecule test

# Test specific role
cd roles/common && molecule test
cd roles/security && molecule test

# Test specific scenario steps
molecule create      # Create test containers
molecule converge    # Run playbook
molecule verify      # Run verification
molecule destroy     # Clean up
```

## Test Scenarios

### Default Molecule Scenario

Tests the full bootstrap process with:
- Ubuntu 20.04, 22.04, and 24.04
- Basic security configuration
- Essential packages
- Development tools (subset)

### Role-Specific Tests

#### Common Role
- Essential package installation
- System configuration (timezone, locale)
- Performance optimizations
- Repository management

#### Security Role
- SSH hardening
- Fail2ban configuration
- Password manager installation
- Automatic updates
- Kernel hardening (when not in container)

## Writing New Tests

### Molecule Tests

1. Create a new scenario:
```bash
cd roles/your-role
molecule init scenario -s your-scenario
```

2. Configure `molecule.yml`, `converge.yml`, and `verify.yml`

3. Run the test:
```bash
molecule test -s your-scenario
```

### Python Tests

1. Create test file in `tests/test_*.py`
2. Use pytest fixtures from `conftest.py`
3. Follow existing test patterns

### Integration Tests

Run the integration test locally (requires sudo):

```bash
ansible-playbook tests/test_integration.yml --ask-become-pass
```

## CI/CD

The project uses GitHub Actions for continuous integration:

- Runs on every push and pull request
- Tests multiple Ubuntu versions
- Runs linting, Python tests, and Molecule tests
- Security scanning with Trivy

## Debugging Failed Tests

### Molecule Debugging

```bash
# Keep containers running after failure
molecule test --destroy=never

# Login to test container
molecule login -h ubuntu-2204

# Re-run specific step
molecule converge
molecule verify
```

### Viewing Ansible Output

```bash
# Verbose output
molecule converge -- -vvv

# Show diff
molecule converge -- --diff
```

## Pre-commit Hooks

Install pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

This will run linting automatically before commits.

## Test Coverage Goals

- All roles should have basic Molecule tests
- Python code should have >80% coverage
- All playbooks should pass ansible-lint
- All YAML files should pass yamllint