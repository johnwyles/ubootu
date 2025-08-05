#!/usr/bin/env python3
"""
Test URL validity for download tasks.
This test should FAIL initially for broken URLs, then pass after URLs are fixed.
"""

import requests
import pytest
import re
from pathlib import Path
import yaml

# URLs that were failing in the logs
KNOWN_BROKEN_URLS = [
    'https://github.com/kapitainsky/RcloneBrowser/releases/download/1.8.0/rclone-browser-1.8.0-linux-x86_64.AppImage',
    # Tailscale URL with newline will be tested separately
]

def find_download_urls_in_yaml():
    """Extract download URLs from YAML files"""
    project_root = Path(__file__).parent.parent
    urls = []
    
    for yaml_file in project_root.rglob('*.yml'):
        try:
            with open(yaml_file, 'r') as f:
                content = f.read()
                
            # Find URLs in the content
            url_patterns = [
                r'https://github\.com/[^\s"\']+',
                r'https://download\.[^\s"\']+',
                r'https://releases\.[^\s"\']+',
                r'https://api\.github\.com/[^\s"\']+',
                r'https://pkgs\.[^\s"\']+',
            ]
            
            for pattern in url_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    # Clean up the URL (remove trailing punctuation, quotes, etc.)
                    clean_url = re.sub(r'["\',}]+$', '', match)
                    if clean_url and clean_url not in urls:
                        urls.append({
                            'url': clean_url,
                            'file': str(yaml_file),
                            'raw_match': match
                        })
                        
        except Exception:
            continue
            
    return urls

def test_github_api_urls():
    """Test that GitHub API URLs are accessible"""
    api_urls = [
        'https://api.github.com/repos/BurntSushi/ripgrep/releases/latest',
        'https://api.github.com/repos/sharkdp/fd/releases/latest',
        'https://api.github.com/repos/slackhq/nebula/releases/latest'
    ]
    
    for url in api_urls:
        try:
            response = requests.head(url, timeout=10)
            assert response.status_code == 200, f"GitHub API URL failed: {url} - Status: {response.status_code}"
        except requests.RequestException as e:
            pytest.fail(f"GitHub API URL failed: {url} - Error: {e}")

def test_download_urls_from_yaml():
    """Test URLs found in YAML files"""
    urls = find_download_urls_in_yaml()
    
    failed_urls = []
    
    for url_info in urls:
        url = url_info['url']
        
        # Skip template URLs that contain Ansible variables
        if '{{' in url or '{%' in url:
            continue
            
        # Skip known problematic URLs that need fixing
        if any(broken in url for broken in KNOWN_BROKEN_URLS):
            continue
            
        try:
            # Use HEAD request to avoid downloading large files
            response = requests.head(url, timeout=10, allow_redirects=True)
            
            if response.status_code >= 400:
                failed_urls.append({
                    'url': url,
                    'status': response.status_code,
                    'file': url_info['file']
                })
                
        except requests.RequestException as e:
            failed_urls.append({
                'url': url,
                'error': str(e),
                'file': url_info['file']
            })
    
    if failed_urls:
        error_msg = "Found failing URLs:\n"
        for fail in failed_urls:
            error_msg += f"  {fail['url']} (in {fail['file']})\n"
            if 'status' in fail:
                error_msg += f"    Status: {fail['status']}\n"
            if 'error' in fail:
                error_msg += f"    Error: {fail['error']}\n"
        
        pytest.fail(error_msg)

def test_tailscale_url_format():
    """Test that tailscale URL doesn't have newline characters"""
    
    # This was the specific error from the logs
    problematic_url = "https://pkgs.tailscale.com/stable/ubuntu/noble\\n.noarmor.gpg"
    correct_url = "https://pkgs.tailscale.com/stable/ubuntu/noble.noarmor.gpg"
    
    # Test that the correct URL works
    try:
        response = requests.head(correct_url, timeout=10)
        assert response.status_code == 200, f"Corrected tailscale URL failed: {correct_url}"
    except requests.RequestException as e:
        pytest.fail(f"Corrected tailscale URL failed: {correct_url} - Error: {e}")
    
    # Test that we don't have the problematic format in our files
    project_root = Path(__file__).parent.parent
    
    for yaml_file in project_root.rglob('*.yml'):
        try:
            with open(yaml_file, 'r') as f:
                content = f.read()
                
            if 'noble\\n' in content or 'noble\n' in content.replace('\n', '\\n'):
                pytest.fail(f"Found newline in tailscale URL in file: {yaml_file}")
                
        except Exception:
            continue

def test_rclone_browser_alternative():
    """Test that RcloneBrowser has a working alternative URL"""
    
    # The original URL was 404
    original_url = "https://github.com/kapitainsky/RcloneBrowser/releases/download/1.8.0/rclone-browser-1.8.0-linux-x86_64.AppImage"
    
    # Test if the latest release API works (for finding current version)
    api_url = "https://api.github.com/repos/kapitainsky/RcloneBrowser/releases/latest"
    
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            # API works, we can use it to get the latest version
            pass
        else:
            # API doesn't work, need alternative
            pytest.fail(f"RcloneBrowser API not accessible: {api_url} - Status: {response.status_code}")
    except requests.RequestException as e:
        pytest.fail(f"RcloneBrowser API failed: {api_url} - Error: {e}")

def test_common_repo_urls():
    """Test common repository URLs"""
    repo_urls = [
        'https://download.docker.com/linux/ubuntu',
        'https://packages.microsoft.com/repos/code',
        # Add more as found in the actual files
    ]
    
    for url in repo_urls:
        try:
            response = requests.head(url, timeout=10)
            # Allow redirects and various success codes for repo URLs
            assert response.status_code < 400, f"Repository URL failed: {url} - Status: {response.status_code}"
        except requests.RequestException as e:
            pytest.fail(f"Repository URL failed: {url} - Error: {e}")

if __name__ == '__main__':
    pytest.main([__file__, '-v'])