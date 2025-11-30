r"""Simple demo showing the legacy Win32 popup menu created by SysTrayIcon.

Run on Windows:
    python demos\demo_simple.py

This demo creates a tray icon with two menu items and logs actions to stdout.
"""

from infi.systray import SysTrayIcon
import time


def on_example(systray):
    print("Example action executed")


def on_about(systray):
    print("About selected")


def on_quit(systray):
    print("Quitting demo")


def main():
    menu_options = (
        ("Example", None, on_example),
        ("About", None, on_about),
    )
    systray = SysTrayIcon(None, "infi.systray demo", menu_options, on_quit)
    systray.start()
    try:
        # Keep the main thread alive; the tray runs on its own thread.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        systray.shutdown()


if __name__ == "__main__":
    main()
