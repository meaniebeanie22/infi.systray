# Dark Mode Implementation Summary

## What Changed

The `infi.systray` package now provides **automatic Windows 11 dark mode support** for system tray menus, matching the appearance of system applications like Windows Defender, Bluetooth settings, and Bitwarden.

## How It Works

### 1. DWM (Desktop Window Manager) Dark Mode Theming

The implementation uses `DwmSetWindowAttribute()` with `DWMWA_USE_IMMERSIVE_DARK_MODE (20)` to enable dark mode on the tray window. This causes Windows to automatically render all menus in the system theme.

**Key function:** `win11_adapter.enable_dark_mode(hwnd)`

```python
def enable_dark_mode(hwnd: int) -> bool:
    """Enable Windows 11 dark mode for a window."""
    dwmapi = ctypes.windll.dwmapi
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    value = ctypes.c_int(1)
    hr = dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, 
                                      ctypes.byref(value), ctypes.sizeof(ctypes.c_int))
    return hr == 0
```

### 2. Automatic Window Initialization

The `traybar.py` module calls `enable_dark_mode()` automatically after creating the window:

```python
def _create_window(self):
    # ... create window ...
    UpdateWindow(self._hwnd)
    
    # Enable dark mode for this window so menus respect system theme
    try:
        from . import win11_adapter
        win11_adapter.enable_dark_mode(self._hwnd)
    except Exception:
        pass
    
    self._refresh_icon()
```

## No Configuration Needed

Users simply create a `SysTrayIcon` normally:

```python
from infi.systray import SysTrayIcon

menu_options = (
    ("Action 1", None, callback1),
    ("Action 2", None, callback2),
)

systray = SysTrayIcon(icon_path, "Hover text", menu_options)
systray.start()
```

When running on Windows 11 with dark mode enabled, the menu will **automatically** render in dark mode matching the system theme.

## Changes Made

### Files Modified

1. **`src/infi/systray/win11_adapter.py`**
   - Removed all file integration code (IContextMenu, PIDL, shell namespace)
   - Added `enable_dark_mode(hwnd: int) -> bool` function
   - Simplified to focus on window-level dark mode support
   - Kept `show_shell_menu()` for menu display

2. **`src/infi/systray/traybar.py`**
   - Added dark mode enable call in `_create_window()` method
   - Removed IContextMenu message forwarding from `WndProc()`
   - Simplified window procedure

3. **`demos/demo_shell_menu.py`**
   - Updated to demonstrate dark mode menus
   - Removed file path handling
   - Shows that menus automatically respect system theme

4. **`README.md`**
   - Updated demo section to explain dark mode support
   - Removed file menu integration documentation
   - Noted that dark mode is automatic (no configuration)

### Files Deleted

- `DARK_MODE_NOTES.md` (no longer needed)

## How Dark Mode Works

When `DWMWA_USE_IMMERSIVE_DARK_MODE` is set on a window:

1. Windows 11 monitors the system dark mode setting
2. When the user right-clicks the tray icon, Windows creates the menu
3. Windows automatically renders the menu in the appropriate theme (dark or light)
4. All text, icons, and backgrounds are handled by the OS

This is exactly how system applications work, providing a native, consistent experience.

## Compatibility

- **Windows 11**: Full dark mode support
- **Windows 10**: Graceful degradation (menus still work, just light-colored)
- **Non-Windows**: Code paths protected with `is_windows()` checks

## Benefits

✓ Respects Windows system theme
✓ Matches Windows Defender, Bitwarden, system apps
✓ No configuration or setup required
✓ Automatic - just use `SysTrayIcon` normally
✓ Uses official Windows APIs (DWM)
✓ Works with any menu structure

## Usage Example

```python
import threading
import time
from infi.systray import SysTrayIcon

def action1(systray):
    print("Action 1 selected")

def action2(systray):
    print("Action 2 selected")

menu_options = (
    ("Action 1", None, action1),
    ("Action 2", None, action2),
)

systray = SysTrayIcon(None, "My App", menu_options)
systray.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    systray.shutdown()
```

When Windows is in dark mode, the menu will render in dark mode automatically!
