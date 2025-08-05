#!/usr/bin/env python3
"""
Integration test for complete Ansible playbook success.
This test should FAIL initially due to remaining issues, then pass after all fixes.
"""

import subprocess
import tempfile
import yaml
import pytest
import re
from pathlib import Path

def test_ansible_syntax_check():
    """Test that the main playbook passes syntax check"""
    project_root = Path(__file__).parent.parent
    
    result = subprocess.run([
        'ansible-playbook',
        str(project_root / 'site.yml'),
        '--syntax-check'
    ], capture_output=True, text=True, cwd=str(project_root))
    
    assert result.returncode == 0, f"Syntax check failed: {result.stderr}"

def test_ansible_check_mode():
    """Test playbook in check mode (dry run) with minimal variables"""
    project_root = Path(__file__).parent.parent
    
    # Create minimal test variables
    test_vars = {
        'primary_user': 'testuser',
        'selected_items': ['git', 'vim'],
        'desktop_environment': 'gnome',
        'de_environment': 'gnome',
        'system_swappiness': 10,
        'enable_firewall': True,
        'ssh_port': 22,
        'ssh_permit_root_login': False,
        'ssh_password_authentication': True,
        'ssh_client_alive_interval': 300,
        'ssh_client_alive_count_max': 3,
        'ssh_max_auth_tries': 3,
        'ssh_max_sessions': 10,
        'ssh_allowed_users': ['testuser'],
        # Add more variables as needed
        'devtools_selected_file_managers': [],
        'devtools_selected_system_monitoring': [],
        'devtools_selected_network_tools': [],
        'devtools_selected_text_processing': [],
        'devtools_selected_dev_cli_tools': [],
        'devtools_selected_productivity_tools': [],
        'devtools_selected_modern_replacements': [],
        'code_editors': ['vim'],
        'prompt_decorator': 'default'
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(test_vars, f)
        vars_file = f.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
        f.write("[local]\nlocalhost ansible_connection=local\n")
        inventory_file = f.name
    
    # Run in check mode
    result = subprocess.run([
        'ansible-playbook',
        str(project_root / 'site.yml'),
        '--check',
        '-i', inventory_file,
        '-e', f'@{vars_file}',
        '--become-password-file', '/dev/null'  # Dummy password file for check mode
    ], capture_output=True, text=True, cwd=str(project_root))
    
    # Check for specific failure patterns
    assert 'is undefined' not in result.stderr, f"Found undefined variables: {result.stderr}"
    assert 'apt_key' not in result.stderr, f"Found apt-key usage: {result.stderr}"
    
    # In check mode, some failures are expected (missing packages, etc.)
    # But critical syntax/variable errors should not occur

def test_no_critical_failures_in_recent_run():
    """Test that the most recent run has no critical FAILED messages"""
    
    log_file = Path('/tmp/ubootu_emergency.log')
    if not log_file.exists():
        pytest.skip("No recent run log found")
    
    with open(log_file, 'r') as f:
        log_content = f.read()
    
    # Get the most recent run (after last "Starting ansible")
    recent_runs = log_content.split('[')
    if len(recent_runs) < 2:
        pytest.skip("No recent run found in log")
    
    most_recent = '[' + recent_runs[-1]
    
    # Count FAILED messages (excluding expected ones)
    failed_lines = []
    for line in most_recent.split('\n'):
        if 'FAILED!' in line:
            # Skip expected failures
            if any(skip in line for skip in [
                'pkill -f unattended-upgrade',  # Expected process cleanup failure
                'could not find job',  # Async job cleanup
            ]):
                continue
            failed_lines.append(line.strip())
    
    # Categorize failures
    critical_failures = []
    minor_failures = []
    
    for failure in failed_lines:
        if any(critical in failure for critical in [
            'is undefined',
            'apt_key',
            'syntax error',
            'duplicate loop'
        ]):
            critical_failures.append(failure)
        else:
            minor_failures.append(failure)
    
    # Critical failures should be zero
    assert len(critical_failures) == 0, f"Found critical failures: {critical_failures}"
    
    # Total failures should be reduced significantly
    total_failures = len(failed_lines)
    assert total_failures < 10, f"Too many failures ({total_failures}). Recent failures: {failed_lines[:5]}"

def test_exit_code_tracking():
    """Test that recent runs are completing with better exit codes"""
    
    debug_log = Path('/tmp/thread_debug.log')
    if not debug_log.exists():
        pytest.skip("No thread debug log found")
    
    with open(debug_log, 'r') as f:
        content = f.read()
    
    # Find recent exit codes
    exit_code_lines = [line for line in content.split('\n') if 'Thread ending, exit_code=' in line]
    
    if not exit_code_lines:
        pytest.skip("No exit codes found in debug log")
    
    # Get the most recent exit code
    recent_exit_code = exit_code_lines[-1]
    
    # Extract the exit code number
    exit_code_match = re.search(r'exit_code=(\d+)', recent_exit_code)
    if exit_code_match:
        exit_code = int(exit_code_match.group(1))
        assert exit_code == 0, f"Most recent run failed with exit code {exit_code}. Expected 0 for complete success."

def test_yaml_lint_passes():
    """Test that YAML files pass linting"""
    project_root = Path(__file__).parent.parent
    
    # Test a few critical YAML files
    critical_files = [
        'site.yml',
        'roles/security/tasks/ssh.yml',
        'roles/desktop-environment/tasks/settings-gnome.yml'
    ]
    
    for file_path in critical_files:
        full_path = project_root / file_path
        if full_path.exists():
            result = subprocess.run([
                'yamllint', str(full_path)
            ], capture_output=True, text=True)
            
            # yamllint returns 0 for success, 1 for warnings, 2+ for errors
            assert result.returncode < 2, f"YAML lint errors in {file_path}: {result.stdout}"

def test_expected_vs_actual_performance():
    """Test performance metrics vs expectations"""
    
    log_file = Path('/tmp/ubootu_emergency.log')
    if not log_file.exists():
        pytest.skip("No recent run log found")
    
    with open(log_file, 'r') as f:
        log_content = f.read()
    
    # Find timestamp range for most recent run
    timestamps = re.findall(r'\[(\d{2}:\d{2}:\d{2})\]', log_content)
    
    if len(timestamps) >= 2:
        start_time = timestamps[0]
        end_time = timestamps[-1]
        
        # Parse times (simplified)
        start_parts = start_time.split(':')
        end_parts = end_time.split(':')
        
        start_minutes = int(start_parts[0]) * 60 + int(start_parts[1])
        end_minutes = int(end_parts[0]) * 60 + int(end_parts[1])
        
        duration = end_minutes - start_minutes
        if duration < 0:  # Crossed hour boundary
            duration += 60
        
        # Should complete in reasonable time (less than 60 minutes for full run)
        assert duration < 60, f"Playbook took too long: {duration} minutes"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])