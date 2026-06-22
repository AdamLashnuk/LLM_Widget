import sys
import os

def get_asset_path(relative_path):
    """Get absolute path to an asset, handling both dev and PyInstaller environments."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Normal Python execution: go up one level from app/utils.py to reach the root
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)