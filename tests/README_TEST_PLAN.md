# Test Plan to Reach 90% Coverage

## Current Status
- **Current Coverage**: 41.99%
- **Target Coverage**: 90.00%
- **Coverage Gap**: 48.01%
- **Failing Tests**: 33
- **Passing Tests**: 278

## Priority Modules for Testing (Lowest Coverage First)

### Critical Low Coverage Modules (< 20%)
1. **overlay_dialog.py** (3.80%)
   - Need to test OverlayDialog class
   - Test dialog creation, rendering, event handling
   
2. **tui_dialogs.py** (5.70%)
   - Test all dialog types (Info, Error, Warning, Confirm, Input)
   - Test dialog lifecycle and user interactions
   
3. **quick_actions_tui.py** (6.02%)
   - Test quick action registration and execution
   - Test menu rendering and navigation
   
4. **help_viewer.py** (9.47%)
   - Test help content loading and display
   - Test navigation between help topics
   
5. **terminal_check.py** (10.42%)
   - Test terminal capability detection
   - Test different terminal environments
   
6. **tui/core.py** (11.69%)
   - Test main TUI application lifecycle
   - Test initialization and cleanup
   
7. **history_viewer.py** (12.68%)
   - Test history entry storage and retrieval
   - Test history display and filtering
   
8. **tui/menu_structure.py** (13.14%)
   - Test menu building from all builders
   - Test menu item relationships
   
9. **menu_ui.py** (15.59%)
   - Test Rich-based menu UI
   - Test menu navigation and selection
   
10. **tui_components.py** (15.32%)
    - Test all UI components (Button, TextField, etc.)
    - Test component rendering and interactions

### Medium Coverage Modules (20-50%)
- backup_config_tui.py (20.83%)
- profile_selector.py (19.77%)
- profile_manager.py (23.20%)
- tui/dialogs.py (23.87%)
- section_selector.py (24.00%)
- app_defaults.py (25.71%)
- backup_config_tui.py (33.33%)
- show_profile_templates.py (40.28%)
- menu_dialog.py (41.04%)
- apt_fixer.py (41.18%)
- config_validator.py (41.98%)
- app_customization_templates.py (43.42%)
- config_models.py (49.83%)

### High Coverage Modules (> 70%) - Minor improvements needed
- terminal_customization.py (67.01%)
- ubootu_splash.py (69.61%)
- tui_splash.py (72.03%)
- tui/menus/base.py (72.97%)
- tui/handlers.py (73.37%)
- tui/renderer.py (78.49%)

### Already at 100% Coverage
- error_handling.py
- tui/__init__.py
- tui/colors.py
- tui/menus/__init__.py
- tui/menus/applications.py
- tui/menus/desktop.py
- tui/menus/development.py
- tui/menus/security.py
- tui/menus/system.py
- tui/models.py

## Test Strategy

### Phase 1: Fix Failing Tests (33 tests)
1. Fix import errors in integration tests
2. Fix API mismatches in TUI tests
3. Update test expectations to match actual implementations

### Phase 2: Test Critical Low Coverage Modules
Focus on modules with < 20% coverage as they provide the most coverage gain

### Phase 3: Test Medium Coverage Modules
Improve modules in the 20-50% range

### Phase 4: Polish High Coverage Modules
Minor improvements to get 70%+ modules to 90%+

## Implementation Approach

For each module:
1. Analyze the module's public API
2. Write unit tests for all public functions/methods
3. Test error conditions and edge cases
4. Test integration points with other modules
5. Mock external dependencies (curses, subprocess, file I/O)

## Estimated Effort
- Fix failing tests: 2-3 hours
- Test low coverage modules: 8-10 hours  
- Test medium coverage modules: 6-8 hours
- Polish high coverage modules: 2-3 hours
- Total: 18-24 hours of focused testing work