"""Pytest configuration and fixtures"""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests"""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def mock_ansible_vars():
    """Mock Ansible variables for testing"""
    return {
        'ansible_hostname': 'test-host',
        'ansible_os_family': 'Debian',
        'ansible_distribution': 'Ubuntu',
        'ansible_distribution_version': '22.04',
        'ansible_distribution_release': 'jammy',
        'ansible_memtotal_mb': 16384,
        'ansible_processor_vcpus': 8,
        'ansible_virtualization_type': 'none',
        'ansible_date_time': {
            'date': '2024-01-01'
        }
    }