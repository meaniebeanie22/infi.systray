import os
import tempfile
import pytest

from infi.systray import win11_adapter


skip_reason = "Requires Windows desktop and comtypes; set RUN_WIN11_UI_TEST=1 to run"


@pytest.mark.skipif(
    not os.name == "nt"
    or not getattr(win11_adapter, "COM_AVAILABLE", False)
    or os.environ.get("RUN_WIN11_UI_TEST") != "1",
    reason=skip_reason,
)
def test_show_shell_menu_for_paths_manual():
    # This is an interactive test — it will show a native shell menu.
    # Run manually on a Windows desktop session with:
    #   SETX RUN_WIN11_UI_TEST 1
    #   pytest -k test_show_shell_menu_for_paths_manual -q
    fd, path = tempfile.mkstemp(suffix=".txt")
    os.close(fd)
    try:
        # Use desktop window as owner (HWND=0) — this will display the menu
        # near the cursor. The test passes if no unhandled exception is raised.
        win11_adapter.show_shell_menu_for_paths(0, [path])
    finally:
        os.remove(path)
