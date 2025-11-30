r"""Demo showing Windows 11 dark mode system tray menus.

This demo shows how the infi.systray menu automatically respects
Windows dark mode when used with Windows 11.

Requirements:
- Windows 11
- System in dark mode (optional, but visually demonstrates the feature)

Run:
    python demos\demo_shell_menu.py

The tray icon will show a menu that automatically renders in dark mode
when Windows is in dark mode, matching the appearance of system menus
like Windows Defender, Bluetooth settings, and Bitwarden.
"""

import os
import sys
import time

from infi.systray import SysTrayIcon


def say_hello(systray):
    print("Hello! This menu respects Windows dark mode.")


def open_url(systray):
    print("This would open a URL (just a demo)")


def on_quit(systray):
    print("Exiting dark mode demo")


def main():
    menu_options = (
        ("Say Hello", None, say_hello),
        ("Open URL", None, open_url),
    )
    systray = SysTrayIcon(None, "Dark Mode Menu Demo", menu_options, on_quit)
    systray.start()
    print("Tray icon created. Right-click to see dark-mode menu.")
    print(
        "Your menu will automatically render in dark mode if Windows is in dark mode."
    )
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        systray.shutdown()


if __name__ == "__main__":
    if os.name != "nt":
        print("This demo only runs on Windows")
        sys.exit(1)
    main()
