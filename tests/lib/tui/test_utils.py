#!/usr/bin/env python3
"""Tests for lib/tui/utils.py"""

import curses
from unittest.mock import MagicMock, Mock, patch, call
import pytest
from lib.tui.utils import (
    center_text,
    draw_box,
    draw_centered_text,
    truncate_text,
    get_dialog_position,
    parse_key,
    key_matches,
)


class TestCenterText:
    """Test center_text function"""

    def test_center_text_basic(self):
        """Test basic text centering"""
        assert center_text(10, "Hi") == 4
        assert center_text(10, "Test") == 3
        assert center_text(20, "Hello") == 7

    def test_center_text_empty_string(self):
        """Test centering empty string"""
        assert center_text(10, "") == 5

    def test_center_text_full_width(self):
        """Test text that fills the width"""
        assert center_text(5, "Hello") == 0

    def test_center_text_longer_than_width(self):
        """Test text longer than width"""
        assert center_text(3, "Hello World") == 0

    def test_center_text_odd_even_lengths(self):
        """Test with odd and even widths/text lengths"""
        assert center_text(11, "Hi") == 4  # Odd width, even text
        assert center_text(10, "Hey") == 3  # Even width, odd text
        assert center_text(11, "Hey") == 4  # Odd width, odd text
        assert center_text(10, "Hi") == 4  # Even width, even text


class TestDrawBox:
    """Test draw_box function"""

    @patch('lib.tui.utils.curses')
    def test_draw_box_basic(self, mock_curses):
        """Test basic box drawing"""
        # Set up mock curses constants
        mock_curses.ACS_ULCORNER = 1
        mock_curses.ACS_URCORNER = 2
        mock_curses.ACS_LLCORNER = 3
        mock_curses.ACS_LRCORNER = 4
        mock_curses.ACS_HLINE = 5
        mock_curses.ACS_VLINE = 6
        mock_curses.A_BOLD = 7
        
        stdscr = MagicMock()
        draw_box(stdscr, 1, 1, 5, 10)

        # Check corners were drawn
        stdscr.addch.assert_any_call(1, 1, 1)  # ULCORNER
        stdscr.addch.assert_any_call(1, 10, 2)  # URCORNER
        stdscr.addch.assert_any_call(5, 1, 3)  # LLCORNER
        stdscr.addch.assert_any_call(5, 10, 4)  # LRCORNER

    @patch('lib.tui.utils.curses')
    def test_draw_box_with_title(self, mock_curses):
        """Test box drawing with title"""
        # Set up mock curses constants
        mock_curses.ACS_ULCORNER = 1
        mock_curses.ACS_URCORNER = 2
        mock_curses.ACS_LLCORNER = 3
        mock_curses.ACS_LRCORNER = 4
        mock_curses.ACS_HLINE = 5
        mock_curses.ACS_VLINE = 6
        mock_curses.A_BOLD = 7
        
        stdscr = MagicMock()
        draw_box(stdscr, 0, 0, 3, 20, title="Test")

        # Check that title was added
        stdscr.attron.assert_called_with(7)  # A_BOLD
        stdscr.attroff.assert_called_with(7)  # A_BOLD
        stdscr.addstr.assert_called()

    @patch('lib.tui.utils.curses.error', Exception)
    def test_draw_box_handles_curses_error(self):
        """Test that draw_box handles curses errors gracefully"""
        stdscr = MagicMock()
        stdscr.addch.side_effect = Exception("curses error")
        # Should not raise exception
        draw_box(stdscr, 0, 0, 5, 10)

    @patch('lib.tui.utils.curses')
    def test_draw_box_lines(self, mock_curses):
        """Test that horizontal and vertical lines are drawn"""
        # Set up mock curses constants
        mock_curses.ACS_ULCORNER = 1
        mock_curses.ACS_URCORNER = 2
        mock_curses.ACS_LLCORNER = 3
        mock_curses.ACS_LRCORNER = 4
        mock_curses.ACS_HLINE = 5
        mock_curses.ACS_VLINE = 6
        
        stdscr = MagicMock()
        draw_box(stdscr, 0, 0, 3, 5)

        # Check horizontal lines (top and bottom)
        for i in range(1, 4):
            stdscr.addch.assert_any_call(0, i, 5)  # ACS_HLINE
            stdscr.addch.assert_any_call(2, i, 5)  # ACS_HLINE

        # Check vertical lines (left and right)
        stdscr.addch.assert_any_call(1, 0, 6)  # ACS_VLINE
        stdscr.addch.assert_any_call(1, 4, 6)  # ACS_VLINE


class TestDrawCenteredText:
    """Test draw_centered_text function"""

    def test_draw_centered_text_basic(self):
        """Test basic centered text drawing"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)
        
        draw_centered_text(stdscr, 10, "Hello")
        
        stdscr.addstr.assert_called_once_with(10, 37, "Hello")

    @patch('lib.tui.utils.curses')
    def test_draw_centered_text_with_bold(self, mock_curses):
        """Test centered text with bold"""
        mock_curses.A_BOLD = 7
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)
        
        draw_centered_text(stdscr, 5, "Bold", bold=True)
        
        stdscr.attron.assert_called_with(7)  # A_BOLD
        stdscr.attroff.assert_called_with(7)  # A_BOLD

    def test_draw_centered_text_with_offset_and_width(self):
        """Test centered text with custom offset and width"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 80)
        
        draw_centered_text(stdscr, 5, "Hi", x_offset=10, width=20)
        
        # Should center within the 20-char width starting at offset 10
        # center_text(20, "Hi") = 9, so x = 10 + 9 = 19
        stdscr.addstr.assert_called_once_with(5, 19, "Hi")

    def test_draw_centered_text_truncates_long_text(self):
        """Test that long text is truncated"""
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (24, 10)
        
        draw_centered_text(stdscr, 5, "This is a very long text")
        
        # Should truncate to fit screen width
        call_args = stdscr.addstr.call_args[0]
        assert len(call_args[2]) <= 10

    @patch('lib.tui.utils.curses.error', Exception)
    def test_draw_centered_text_handles_curses_error(self):
        """Test that draw_centered_text handles curses errors"""
        stdscr = MagicMock()
        stdscr.getmaxyx.side_effect = Exception("curses error")
        # Should not raise exception
        draw_centered_text(stdscr, 5, "Test")


class TestTruncateText:
    """Test truncate_text function"""

    def test_truncate_text_short(self):
        """Test text shorter than max width"""
        assert truncate_text("Hello", 10) == "Hello"

    def test_truncate_text_exact(self):
        """Test text exactly at max width"""
        assert truncate_text("Hello", 5) == "Hello"

    def test_truncate_text_long(self):
        """Test text longer than max width"""
        assert truncate_text("Hello World", 8) == "Hello..."

    def test_truncate_text_custom_suffix(self):
        """Test with custom suffix"""
        assert truncate_text("Hello World", 7, suffix="..") == "Hello.."

    def test_truncate_text_very_short_max_width(self):
        """Test with very short max width"""
        assert truncate_text("Hello", 2) == "He"
        assert truncate_text("Hello", 3) == "Hel"

    def test_truncate_text_empty_string(self):
        """Test with empty string"""
        assert truncate_text("", 10) == ""

    def test_truncate_text_max_width_smaller_than_suffix(self):
        """Test when max width is smaller than suffix"""
        assert truncate_text("Hello World", 2, suffix="...") == "He"


class TestGetDialogPosition:
    """Test get_dialog_position function"""

    def test_get_dialog_position_centered(self):
        """Test dialog centering"""
        y, x = get_dialog_position(24, 80, 10, 40)
        assert y == 7  # (24 - 10) // 2
        assert x == 20  # (80 - 40) // 2

    def test_get_dialog_position_small_screen(self):
        """Test with small screen"""
        y, x = get_dialog_position(10, 20, 8, 15)
        assert y == 1  # (10 - 8) // 2
        assert x == 2  # (20 - 15) // 2

    def test_get_dialog_position_dialog_larger_than_screen(self):
        """Test when dialog is larger than screen"""
        y, x = get_dialog_position(10, 20, 15, 30)
        assert y == 0  # max(0, negative) = 0
        assert x == 0  # max(0, negative) = 0

    def test_get_dialog_position_exact_fit(self):
        """Test when dialog exactly fits screen"""
        y, x = get_dialog_position(10, 20, 10, 20)
        assert y == 0
        assert x == 0


class TestParseKey:
    """Test parse_key function"""

    @patch('lib.tui.utils.curses')
    def test_parse_key_arrow_keys(self, mock_curses):
        """Test parsing arrow keys"""
        mock_curses.KEY_UP = 259
        mock_curses.KEY_DOWN = 258
        mock_curses.KEY_LEFT = 260
        mock_curses.KEY_RIGHT = 261
        
        assert parse_key(259) == "KEY_UP"
        assert parse_key(258) == "KEY_DOWN"
        assert parse_key(260) == "KEY_LEFT"
        assert parse_key(261) == "KEY_RIGHT"

    @patch('lib.tui.utils.curses')
    def test_parse_key_special_keys(self, mock_curses):
        """Test parsing special keys"""
        mock_curses.KEY_F1 = 265
        assert parse_key(265) == "KEY_F1"
        assert parse_key(27) == "ESC"
        assert parse_key(ord("\n")) == "\n"

    def test_parse_key_printable_ascii(self):
        """Test parsing printable ASCII characters"""
        assert parse_key(ord("a")) == "a"
        assert parse_key(ord("Z")) == "Z"
        assert parse_key(ord("1")) == "1"
        assert parse_key(ord(" ")) == " "
        assert parse_key(ord("!")) == "!"

    def test_parse_key_non_printable(self):
        """Test parsing non-printable characters"""
        assert parse_key(0) is None
        assert parse_key(31) is None
        assert parse_key(127) is None
        assert parse_key(200) is None


class TestKeyMatches:
    """Test key_matches function"""

    @patch('lib.tui.utils.parse_key')
    def test_key_matches_with_parsed_key(self, mock_parse):
        """Test key matching with parsed key"""
        mock_parse.return_value = "KEY_UP"
        assert key_matches(259, ["KEY_UP", "k"]) is True
        
        mock_parse.return_value = "KEY_DOWN"
        assert key_matches(258, ["KEY_UP", "k"]) is False

    def test_key_matches_with_char(self):
        """Test key matching with character"""
        assert key_matches(ord("k"), ["KEY_UP", "k"]) is True
        assert key_matches(ord("j"), ["KEY_DOWN", "j"]) is True
        assert key_matches(ord("x"), ["KEY_UP", "k"]) is False

    def test_key_matches_space(self):
        """Test key matching with space"""
        assert key_matches(ord(" "), [" "]) is True

    def test_key_matches_case_sensitive(self):
        """Test that key matching is case sensitive"""
        assert key_matches(ord("q"), ["q", "Q"]) is True
        assert key_matches(ord("Q"), ["q", "Q"]) is True
        assert key_matches(ord("q"), ["Q"]) is False

    @patch('lib.tui.utils.parse_key')
    def test_key_matches_non_printable(self, mock_parse):
        """Test key matching with non-printable key"""
        mock_parse.return_value = None
        assert key_matches(0, ["KEY_UP"]) is False

    def test_key_matches_empty_binding(self):
        """Test with empty binding list"""
        assert key_matches(ord("k"), []) is False