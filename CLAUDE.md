# CLAUDE.md - Ubootu Project Bootstrap

**Ubootu**: Ubuntu configuration tool with curses TUI + Ansible automation

## Core Files
```
configure_standard_tui.py   # Main entry point
lib/tui/unified_menu.py     # Menu system
lib/tui/menu_items.py       # Tool definitions (400+)
roles/*/tasks/*.yml         # Ansible tasks
config.yml                  # User selections (git-ignored)
```

## Commands
```bash
# Run
./configure_standard_tui.py

# Test
source .venv/bin/activate
pytest tests/ -v

# Debug
export DEBUG_TUI=1
tail -f /tmp/debug_tui.log
```

## Key Rules
- Python 3.8+ compatibility (use `Union[]` not `|`)
- Tool IDs: kebab-case (`docker-ce`)
- Always handle `curses.error`
- Test coverage target: 90% (current: 38%)

## Current Issues
- ✅ Fixed: apt-key usage updated to modern signed-by approach
- Some packages need snap alternatives  
- Shell startup errors fixed locally (see git history)
- Test coverage at 35.74% (target: 90%)

## Workflow
1. User selects in TUI → saves to config.yml
2. Ansible reads config.yml → applies changes
3. 3-minute timeout on operations