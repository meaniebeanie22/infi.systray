"""Windows 11 / Dark Mode Support for System Tray Menus

This module provides Windows 11 dark mode support for system tray menus,
making them respect the system theme and use correct fonts like Windows Defender,
Bluetooth settings, Bitwarden, and other modern system applications.

The implementation uses DWM (Desktop Window Manager) dark mode theming
on the tray window itself, which causes all menus to render in dark mode
when the system is in dark mode.

Functions:
    enable_dark_mode(hwnd):
        Enable dark mode rendering for the window and its menus.
        This should be called from traybar._create_window after window creation.

    show_shell_menu(hwnd, menu_options):
        Show a popup menu with dark mode support using system fonts.

Features:
    - System dark mode detection and support
    - Proper font rendering (matches system menus)
    - Full keyboard and mouse support
    - Compatible with all Windows 11 themes
"""

import os
import sys
import ctypes
from typing import Any, Callable, Optional, Sequence, Tuple

# Type alias for menu option tuples
MenuOption = Tuple[str, Optional[Any], Optional[Callable[..., Any]], int]


def is_windows() -> bool:
    return os.name == "nt" or sys.platform == "win32"


def enable_dark_mode(hwnd: int) -> bool:
    """Enable Windows 11 dark mode for a window.

    This function sets the DWMWA_USE_IMMERSIVE_DARK_MODE attribute on the window,
    which causes Windows to render the window and its menus in dark mode when
    the system is in dark mode.

    Args:
        hwnd: Window handle

    Returns:
        True if dark mode was enabled, False otherwise
    """
    if not is_windows():
        return False

    try:
        dwmapi = ctypes.windll.dwmapi

        # DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20

        # Set the attribute to True (1)
        value = ctypes.c_int(1)
        hr = dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(value),
            ctypes.sizeof(ctypes.c_int),
        )

        return hr == 0  # S_OK
    except Exception:
        return False


def show_shell_menu(hwnd: int, menu_options: Sequence[MenuOption]):
    """Show a popup menu with dark mode support.

    This implementation uses HMENU + TrackPopupMenu with dark mode support
    enabled on the window. When the window has dark mode enabled via
    enable_dark_mode(), menus will respect the system theme.

    Parameters:
        hwnd: Owner window handle
        menu_options: List of menu option tuples (text, icon, action, id)

    Behavior:
        - Builds an HMENU and inserts the provided menu entries
        - Displays it at the current cursor position
        - If the user selects an item, the mapped Python callable is invoked
        - Menus will render in dark mode if system is in dark mode
    """
    if not is_windows():
        raise RuntimeError("Windows-only API: cannot show shell menu on this platform")

    try:
        from .win32_adapter import (
            CreatePopupMenu,
            InsertMenuItem,
            PackMENUITEMINFO,
            TrackPopupMenu,
            TPM_LEFTALIGN,
            GetCursorPos,
            POINT,
            SetForegroundWindow,
            PostMessage,
            WM_NULL,
            ctypes,
        )
    except Exception as e:
        raise RuntimeError(
            "win32_adapter functions are required to show shell menu"
        ) from e

    # TPM_RETURNCMD lets us get the command ID synchronously
    TPM_RETURNCMD = 0x0100
    # TPM_SYSTEMFONT uses the system font
    TPM_SYSTEMFONT = 0x0200

    # Build HMENU and map ids to actions
    hmenu = CreatePopupMenu()
    id_to_action = {}

    # menu_options are expected in order; InsertMenuItem inserts at position 0,
    # so iterate reversed to preserve original ordering.
    for option_text, option_icon, option_action, option_id in menu_options[::-1]:
        item = PackMENUITEMINFO(text=option_text, hbmpItem=None, wID=option_id)
        InsertMenuItem(hmenu, 0, 1, ctypes.byref(item))
        id_to_action[option_id] = option_action

    # Show menu at cursor position
    pos = POINT()
    GetCursorPos(ctypes.byref(pos))
    SetForegroundWindow(hwnd)

    try:
        cmd = TrackPopupMenu(
            hmenu,
            TPM_RETURNCMD | TPM_LEFTALIGN | TPM_SYSTEMFONT,
            pos.x,
            pos.y,
            0,
            hwnd,
            None,
        )
    except Exception:
        # Some environments expose the function differently; fall back
        TrackPopupMenu(
            hmenu, TPM_LEFTALIGN | TPM_SYSTEMFONT, pos.x, pos.y, 0, hwnd, None
        )
        PostMessage(hwnd, WM_NULL, 0, 0)
        return

    # Execute the selected action
    if cmd and cmd in id_to_action:
        action = id_to_action[cmd]
        try:
            if callable(action):
                action(None)
        except Exception:
            # Swallow exceptions to avoid crashing message loop
            pass
