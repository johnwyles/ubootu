# Ubootu TUI Architecture

The TUI has been refactored into a modular structure for better maintainability:

## Module Structure

### `menu_structure.py`
- `MenuItem` dataclass definition
- `build_menu_structure()` - Creates the hierarchical menu tree

### `colors.py`
- Color constants (COLOR_HEADER, COLOR_SELECTED, etc.)
- `init_colors()` - Initializes curses color pairs
- `get_category_color()` - Returns color based on selection status

### `ui_renderer.py`
- `UIRenderer` class containing all drawing methods:
  - `draw_header()` - Draws the title and selection count
  - `draw_menu()` - Draws the menu items with indicators
  - `draw_help()` - Draws the F-key help bar
  - `draw_stats()` - Draws selection statistics
  - `draw_breadcrumb()` - Draws navigation breadcrumb

### `dialogs.py`
- `DialogManager` class for popup dialogs:
  - `show_actions_popup()` - F1 actions menu
  - `show_slider_dialog()` - Configuration sliders
  - `show_confirmation_dialog()` - Yes/No dialogs
  - `show_error_dialog()` - Error messages

### `input_handler.py`
- `InputHandler` class for keyboard input:
  - `handle_key()` - Main key dispatcher
  - `handle_navigation()` - Arrow keys, page up/down
  - `handle_selection()` - Space, Enter keys
  - `handle_function_keys()` - F1-F10

### `actions.py`
- `ActionHandler` class for menu actions:
  - `handle_install()` - Start installation
  - `handle_save()` - Save configuration
  - `handle_reset()` - Reset selections
  - `handle_exit()` - Exit confirmation

### `app.py`
- `UbootuTUI` main application class that ties everything together
- Manages the main loop and coordinates between modules

### `__init__.py`
- Exports the main `UbootuTUI` class for easy importing

## Key Design Principles

1. **Separation of Concerns**: Each module has a single responsibility
2. **Loose Coupling**: Modules communicate through well-defined interfaces
3. **High Cohesion**: Related functionality is grouped together
4. **Easy Testing**: Each module can be tested independently
5. **Clear Dependencies**: No circular imports, clear hierarchy

## Usage

```python
from lib.tui import UbootuTUI
import curses

def main(stdscr):
    app = UbootuTUI(stdscr)
    return app.run()

curses.wrapper(main)
```