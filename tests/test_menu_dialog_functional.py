#!/usr/bin/env python3
"""
Functional tests for menu_dialog module
Tests the TUI menu dialog components
"""

import curses
from unittest.mock import MagicMock, Mock, call, patch

import pytest

# Mock curses constants that aren't available without initscr
if not hasattr(curses, 'ACS_ULCORNER'):
    curses.ACS_ULCORNER = ord('+')
    curses.ACS_URCORNER = ord('+')
    curses.ACS_LLCORNER = ord('+')
    curses.ACS_LRCORNER = ord('+')
    curses.ACS_HLINE = ord('-')
    curses.ACS_VLINE = ord('|')
    curses.A_BOLD = 1
    curses.A_DIM = 2
    curses.A_REVERSE = 4
    curses.KEY_UP = 259
    curses.KEY_DOWN = 258

from lib.menu_dialog import HelpOverlay, KeyHintBar, MenuDialog, QuickMenu


class TestKeyHintBar:
    """Test KeyHintBar functionality"""

    def setup_method(self):
        """Setup mock stdscr"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)

    def test_init(self):
        """Test KeyHintBar initialization"""
        hint_bar = KeyHintBar(self.stdscr)
        
        assert hint_bar.stdscr == self.stdscr
        assert hint_bar.height == 24
        assert hint_bar.width == 80

    def test_draw_hints(self):
        """Test drawing key hints"""
        hint_bar = KeyHintBar(self.stdscr)
        hints = [("ESC", "Exit"), ("ENTER", "Select")]
        
        hint_bar.draw(hints, 10)
        
        # Should have called addstr with the hints
        self.stdscr.addstr.assert_called()
        call_args = self.stdscr.addstr.call_args[0]
        assert call_args[0] == 10  # y position
        assert "ESC:Exit" in call_args[2]
        assert "ENTER:Select" in call_args[2]

    def test_draw_hints_truncated(self):
        """Test that long hints are truncated"""
        hint_bar = KeyHintBar(self.stdscr)
        hint_bar.width = 20  # Small width
        
        hints = [("A", "Very long description that will be truncated")]
        hint_bar.draw(hints, 5)
        
        self.stdscr.addstr.assert_called()
        call_args = self.stdscr.addstr.call_args[0]
        hint_str = call_args[2]
        assert len(hint_str) <= 18  # width - 2
        assert "..." in hint_str

    def test_draw_handles_curses_error(self):
        """Test that curses errors are handled"""
        hint_bar = KeyHintBar(self.stdscr)
        self.stdscr.addstr.side_effect = curses.error
        
        # Should not raise exception
        hint_bar.draw([("ESC", "Exit")], 10)


class TestHelpOverlay:
    """Test HelpOverlay functionality"""

    def setup_method(self):
        """Setup mock stdscr"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)

    def test_init(self):
        """Test HelpOverlay initialization"""
        overlay = HelpOverlay(self.stdscr)
        
        assert overlay.stdscr == self.stdscr
        assert overlay.height == 24
        assert overlay.width == 80

    def test_show_help(self):
        """Test showing help overlay"""
        overlay = HelpOverlay(self.stdscr)
        self.stdscr.getch.return_value = ord(' ')  # Space key
        
        title = "Help"
        content = ["Line 1", "Line 2", "Line 3"]
        
        overlay.show(title, content)
        
        # Should clear screen
        self.stdscr.clear.assert_called()
        
        # Should draw title
        addstr_calls = self.stdscr.addstr.call_args_list
        assert any("Help" in str(call) for call in addstr_calls)
        
        # Should draw content lines
        assert any("Line 1" in str(call) for call in addstr_calls)
        assert any("Line 2" in str(call) for call in addstr_calls)
        
        # Should wait for key press
        self.stdscr.getch.assert_called()
        self.stdscr.refresh.assert_called()

    def test_show_help_truncates_long_lines(self):
        """Test that long lines are truncated"""
        overlay = HelpOverlay(self.stdscr)
        overlay.width = 20
        
        content = ["This is a very long line that should be truncated"]
        overlay.show("Test", content)
        
        # Line should be truncated to width - 4
        addstr_calls = self.stdscr.addstr.call_args_list
        for call in addstr_calls:
            if len(call[0]) >= 3:
                line = call[0][2]
                if isinstance(line, str) and "very long" in line:
                    assert len(line) <= 16

    def test_show_handles_curses_error(self):
        """Test that curses errors are handled"""
        overlay = HelpOverlay(self.stdscr)
        self.stdscr.addstr.side_effect = curses.error
        self.stdscr.getch.return_value = ord(' ')
        
        # Should not raise exception
        overlay.show("Help", ["Content"])


class TestMenuDialog:
    """Test MenuDialog functionality"""

    def setup_method(self):
        """Setup mock stdscr"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)
        self.stdscr.getch.return_value = ord('\n')  # Default to Enter key

    @patch('lib.menu_dialog.curses.curs_set')
    def test_init(self, mock_curs_set):
        """Test MenuDialog initialization"""
        dialog = MenuDialog(self.stdscr)
        
        assert dialog.stdscr == self.stdscr
        assert dialog.height == 24
        assert dialog.width == 80
        assert isinstance(dialog.key_hints, KeyHintBar)
        assert isinstance(dialog.help_overlay, HelpOverlay)
        
        # Should hide cursor - tested in the patch

    def test_draw_box(self):
        """Test drawing a box"""
        with patch('lib.menu_dialog.curses.curs_set'):
            dialog = MenuDialog(self.stdscr)
        
        dialog.draw_box(5, 10, 10, 20, "Title")
        
        # Should draw corners
        self.stdscr.addch.assert_any_call(5, 10, curses.ACS_ULCORNER)
        self.stdscr.addch.assert_any_call(5, 29, curses.ACS_URCORNER)
        self.stdscr.addch.assert_any_call(14, 10, curses.ACS_LLCORNER)
        self.stdscr.addch.assert_any_call(14, 29, curses.ACS_LRCORNER)
        
        # Title should be drawn
        assert self.stdscr.addstr.called

    def test_draw_centered_text(self):
        """Test drawing centered text"""
        with patch('lib.menu_dialog.curses.curs_set'):
            dialog = MenuDialog(self.stdscr)
            dialog.width = 80
        
        dialog.draw_centered_text(10, "Centered Text")
        
        # Text should be centered
        self.stdscr.addstr.assert_called()
        call_args = self.stdscr.addstr.call_args[0]
        assert call_args[0] == 10  # y position
        assert call_args[1] == 33  # Centered x position (80 - 13) // 2
        assert "Centered Text" in call_args[2]

    def test_show_menu_basic(self):
        """Test showing basic menu"""
        with patch('lib.menu_dialog.curses.curs_set'):
            dialog = MenuDialog(self.stdscr)
            self.stdscr.getch.return_value = ord('\n')  # Enter key
        
            items = [
                ("item1", "Item 1", "Description 1"),
                ("item2", "Item 2", "Description 2"),
                ("item3", "Item 3", "Description 3")
            ]
        
            result = dialog.show("Test Menu", items)
        
        assert result == "item1"  # First item selected
        self.stdscr.clear.assert_called()
        self.stdscr.refresh.assert_called()

    def test_show_menu_navigation_down(self):
        """Test navigating down in menu"""
        with patch('lib.menu_dialog.curses.curs_set'):
            dialog = MenuDialog(self.stdscr)
            # Simulate: Down arrow, then Enter
            self.stdscr.getch.side_effect = [curses.KEY_DOWN, ord('\n')]
        
            items = [
                ("item1", "Item 1", ""),
                ("item2", "Item 2", ""),
                ("item3", "Item 3", "")
            ]
        
            result = dialog.show("Test Menu", items)
        
        assert result == "item2"  # Second item selected

    def test_show_menu_navigation_up(self):
        """Test navigating up in menu"""
        with patch('lib.menu_dialog.curses.curs_set'):
            dialog = MenuDialog(self.stdscr)
            # Simulate: Down, Down, Up, Enter
            self.stdscr.getch.side_effect = [
                curses.KEY_DOWN, curses.KEY_DOWN, curses.KEY_UP, ord('\n')
            ]
        
            items = [
                ("item1", "Item 1", ""),
                ("item2", "Item 2", ""),
                ("item3", "Item 3", "")
            ]
        
            result = dialog.show("Test Menu", items)
        
        assert result == "item2"  # Second item selected

    def test_show_menu_escape(self):
        """Test escaping from menu"""
        with patch('lib.menu_dialog.curses.curs_set'):
            dialog = MenuDialog(self.stdscr)
            self.stdscr.getch.return_value = 27  # ESC key
        
            items = [("item1", "Item 1", "")]
        
            result = dialog.show("Test Menu", items)
        
        assert result is None

    def test_show_menu_quit(self):
        """Test quitting with Q key"""
        with patch('lib.menu_dialog.curses.curs_set'):
            dialog = MenuDialog(self.stdscr)
            self.stdscr.getch.return_value = ord('q')
        
            items = [("item1", "Item 1", "")]
        
            result = dialog.show("Test Menu", items)
        
        assert result is None

    def test_show_menu_help(self):
        """Test showing help"""
        with patch('lib.menu_dialog.curses.curs_set'):
            dialog = MenuDialog(self.stdscr)
            # Simulate: H for help, space to close help, then Enter
            self.stdscr.getch.side_effect = [ord('h'), ord(' '), ord('\n')]
        
            items = [("item1", "Item 1", "")]
        
            with patch.object(dialog.help_overlay, 'show') as mock_show:
                result = dialog.show("Test Menu", items)
            
            # Help should be shown
            mock_show.assert_called_once()
            assert result == "item1"

    def test_show_menu_number_selection(self):
        """Test selecting with number keys"""
        with patch('lib.menu_dialog.curses.curs_set'):
            dialog = MenuDialog(self.stdscr)
            self.stdscr.getch.return_value = ord('2')  # Press '2'
        
            items = [
                ("item1", "Item 1", ""),
                ("item2", "Item 2", ""),
                ("item3", "Item 3", "")
            ]
        
            result = dialog.show("Test Menu", items)
        
        assert result == "item2"  # Second item selected

    def test_show_menu_with_header_footer(self):
        """Test menu with header and footer lines"""
        with patch('lib.menu_dialog.curses.curs_set'):
            dialog = MenuDialog(self.stdscr)
            self.stdscr.getch.return_value = ord('\n')
        
            items = [("item1", "Item 1", "")]
            header_lines = ["Header Line 1", "Header Line 2"]
            footer_lines = ["Footer Line 1"]
        
            result = dialog.show(
                "Test Menu",
                items,
                header_lines=header_lines,
                footer_lines=footer_lines
            )
        
        assert result == "item1"
        
        # Check that header and footer were drawn
        addstr_calls = [str(call) for call in self.stdscr.addstr.call_args_list]
        assert any("Header Line 1" in call for call in addstr_calls)
        assert any("Footer Line 1" in call for call in addstr_calls)

    def test_show_menu_scrolling(self):
        """Test menu scrolling with many items"""
        with patch('lib.menu_dialog.curses.curs_set'):
            dialog = MenuDialog(self.stdscr)
            dialog.height = 10  # Small height to force scrolling
        
            # Create many items
            items = [(f"item{i}", f"Item {i}", "") for i in range(20)]
        
            # Simulate scrolling down past visible area
            keys = [curses.KEY_DOWN] * 15 + [ord('\n')]
            self.stdscr.getch.side_effect = keys
        
            result = dialog.show("Test Menu", items)
        
        assert result == "item15"  # 16th item (0-indexed)

    def test_show_menu_on_select_callback(self):
        """Test on_select callback"""
        with patch('lib.menu_dialog.curses.curs_set'):
            dialog = MenuDialog(self.stdscr)
        
            selected_items = []
            def on_select(item_id):
                selected_items.append(item_id)
        
            # Navigate down twice, then select
            self.stdscr.getch.side_effect = [
                curses.KEY_DOWN, curses.KEY_DOWN, ord('\n')
            ]
        
            items = [
                ("item1", "Item 1", ""),
                ("item2", "Item 2", ""),
                ("item3", "Item 3", "")
            ]
        
            result = dialog.show("Test Menu", items, on_select=on_select)
        
        assert result == "item3"
        assert selected_items == ["item2", "item3"]

    def test_show_menu_no_box_mode(self):
        """Test menu without box mode"""
        with patch('lib.menu_dialog.curses.curs_set'):
            dialog = MenuDialog(self.stdscr)
            self.stdscr.getch.return_value = ord('\n')
        
            items = [("item1", "Item 1", "")]
        
            result = dialog.show("Test Menu", items, box_mode=False)
        
        assert result == "item1"
        
        # Should not draw box (no corner characters)
        for call in self.stdscr.addch.call_args_list:
            if len(call[0]) >= 3:
                assert call[0][2] not in [
                    curses.ACS_ULCORNER, curses.ACS_URCORNER,
                    curses.ACS_LLCORNER, curses.ACS_LRCORNER
                ]

    def test_show_menu_empty_items(self):
        """Test menu with no items"""
        with patch('lib.menu_dialog.curses.curs_set'):
            dialog = MenuDialog(self.stdscr)
            # Empty menu should immediately return None without waiting for input
            self.stdscr.getch.return_value = 27  # ESC key just in case
        
            result = dialog.show("Empty Menu", [])
        
        assert result is None


class TestQuickMenu:
    """Test QuickMenu functionality"""

    def setup_method(self):
        """Setup mock stdscr"""
        self.stdscr = MagicMock()
        self.stdscr.getmaxyx.return_value = (24, 80)
        self.stdscr.getch.return_value = ord('\n')

    def test_init(self):
        """Test QuickMenu initialization"""
        with patch('lib.menu_dialog.curses.curs_set'):
            quick_menu = QuickMenu(self.stdscr)
        
            assert isinstance(quick_menu.menu, MenuDialog)

    def test_show_quick_menu(self):
        """Test showing quick menu"""
        with patch('lib.menu_dialog.curses.curs_set'):
            quick_menu = QuickMenu(self.stdscr)
        
            with patch.object(quick_menu.menu, 'show', return_value="opt2") as mock_show:
                options = [
                    ("opt1", "Option 1"),
                    ("opt2", "Option 2"),
                    ("opt3", "Option 3")
                ]
            
                result = quick_menu.show("Quick Select", options)
            
                assert result == "opt2"
            
                # Check that show was called with correct parameters
                mock_show.assert_called_once()
                call_args = mock_show.call_args
                assert call_args[1]['title'] == "Quick Select"
                assert call_args[1]['box_mode'] is False
                assert call_args[1]['allow_help'] is False
            
                # Check items were converted correctly
                items = call_args[1]['items']
                assert len(items) == 3
                assert items[0] == ("opt1", "Option 1", "")
                assert items[1] == ("opt2", "Option 2", "")

    def test_show_quick_menu_cancelled(self):
        """Test cancelling quick menu"""
        with patch('lib.menu_dialog.curses.curs_set'):
            quick_menu = QuickMenu(self.stdscr)
        
            with patch.object(quick_menu.menu, 'show', return_value=None):
                options = [("opt1", "Option 1")]
            
                result = quick_menu.show("Quick Select", options)
            
                assert result is None