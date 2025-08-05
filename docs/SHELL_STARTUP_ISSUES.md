# Shell Startup Issues - Debugging Guide

If you're experiencing errors when starting your shell after running Ubootu, this guide will help you diagnose and fix them.

## Common Issues

### 1. "error: invalid value 'ype' for '--type <filetype>'"

This error suggests that somewhere an `fd` command is being called with a malformed argument.

**To debug:**
```bash
# Enable Ubootu shell debugging
export UBOOTU_DEBUG_SHELL=1
# Start a new shell
bash
# Look for [UBOOTU DEBUG] messages
```

**Common causes:**
- Corrupted environment variable (check `env | grep TYPE`)
- Conflicting shell alias or function
- Third-party tool misconfiguration

**Fix:**
```bash
# Check for problematic environment variables
env | grep -i "type.*ype"

# Check your personal shell configs
grep -n "fd.*--type" ~/.bashrc ~/.bash_profile ~/.profile 2>/dev/null

# Temporarily disable custom configs
mv ~/.bashrc ~/.bashrc.backup
# Test if error persists
```

### 2. Permission Denied Warnings for APT Sources

```
WARNING:root:could not open file '/etc/apt/sources.list.d/xxx.list': Permission denied
```

**Cause:** Something is trying to read APT repository files at shell startup without proper permissions.

**Common culprits:**
- Python-based shell prompts (powerline, etc.)
- Custom shell functions that check package status
- Third-party tools that monitor system state

**Fix:**
```bash
# Check what Python modules are being loaded
python3 -c "import sys; print('\n'.join(sys.modules.keys()))" 2>&1 | grep apt

# Disable Python warnings temporarily
export PYTHONWARNINGS="ignore"
```

### 3. "__sdkman_echo_debug: command not found"

**Cause:** SDKMAN initialization is incomplete or there's a version mismatch.

**Fix:**
```bash
# Reinstall SDKMAN
rm -rf ~/.sdkman
curl -s "https://get.sdkman.io" | bash

# Or disable SDKMAN temporarily
# Comment out SDKMAN lines in ~/.bashrc
```

## Diagnostic Steps

1. **Identify when errors occur:**
   ```bash
   # Start shell with verbose output
   bash -xv 2>shell_debug.log
   # Review the log
   less shell_debug.log
   ```

2. **Check Ubootu-managed files:**
   ```bash
   ls -la ~/.config/
   # Look for Ubootu files like:
   # dev-path-config.sh
   # modern-cli-aliases.sh
   # ubootu-shell-debug.sh
   ```

3. **Isolate the issue:**
   ```bash
   # Start shell without configs
   bash --norc
   # If no errors, the issue is in shell configs
   
   # Source configs one by one
   source ~/.bashrc
   # Check for errors after each source
   ```

## Preventive Measures

1. **Before running Ubootu:**
   - Backup your shell configs: `cp ~/.bashrc ~/.bashrc.pre-ubootu`
   - Note any custom tools or prompts you use

2. **After running Ubootu:**
   - Test shell startup immediately
   - Use `UBOOTU_DEBUG_SHELL=1` for first few sessions

3. **Report issues:**
   - Include output of `bash -xv 2>&1 | head -100`
   - List any custom shell tools you use
   - Mention your Ubuntu version

## Quick Fixes

If you need to quickly resolve issues:

```bash
# Disable all Ubootu shell configs temporarily
mkdir ~/ubootu_backup
mv ~/.config/*ubootu* ~/ubootu_backup/ 2>/dev/null
mv ~/.config/dev-path-config.sh ~/ubootu_backup/ 2>/dev/null
mv ~/.config/modern-cli-aliases.sh ~/ubootu_backup/ 2>/dev/null

# Remove Ubootu entries from .bashrc
sed -i.bak '/ubootu\|dev-path-config\|modern-cli-aliases/d' ~/.bashrc

# Test shell
bash
```

## Getting Help

If issues persist:
1. Enable debug mode: `export UBOOTU_DEBUG_SHELL=1`
2. Capture output: `bash -xv 2>debug.log`
3. Create an issue with the debug.log file