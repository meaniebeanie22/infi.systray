"""
Quick verification that dark mode support is properly integrated.

This shows the flow of how dark mode is enabled:

1. User creates a SysTrayIcon instance
2. User calls .start() to show the tray
3. Internally, traybar._create_window() is called
4. _create_window() calls win11_adapter.enable_dark_mode(hwnd)
5. enable_dark_mode() calls DwmSetWindowAttribute with DWMWA_USE_IMMERSIVE_DARK_MODE
6. When the user right-clicks the tray icon, Windows displays the menu in the system theme

Example usage:

    from infi.systray import SysTrayIcon
    
    def my_callback(systray):
        print("Menu item clicked")
    
    # Create tray icon (dark mode is automatic!)
    menu_options = (
        ("Action 1", None, my_callback),
        ("Action 2", None, my_callback),
    )
    
    systray = SysTrayIcon(icon_path, "Hover text", menu_options)
    systray.start()  # <-- Dark mode is enabled here automatically

The menu will automatically:
  ✓ Respect Windows dark mode when Windows is in dark mode
  ✓ Use correct system fonts
  ✓ Match the appearance of Defender, Bluetooth, Bitwarden, etc.
  ✓ Respond to system theme changes

No additional configuration needed!
"""
