r"""Settings persistence to %APPDATA%\OctaveLights\config.json."""

import json
import os
from pathlib import Path


class Config:
    def __init__(self):
        """Load config from %APPDATA%."""
        self.app_data = Path(os.getenv("APPDATA")) / "OctaveLights"
        self.config_file = self.app_data / "config.json"
        self.app_data.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self):
        """Load JSON config, or return defaults."""
        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    return json.load(f)
            except Exception:
                pass
        return self._defaults()

    def _defaults(self):
        """Return default settings."""
        return {
            "enabled": True,
            "color": "white",
            "highlight_pressed": False,
            "highlight_color": "cyan",
            "launch_at_startup": False,
        }

    def save(self):
        """Write config to JSON."""
        with open(self.config_file, "w") as f:
            json.dump(self.data, f, indent=2)

    def get(self, key, default=None):
        """Get a config value."""
        return self.data.get(key, default)

    def set(self, key, value):
        """Set a config value and save."""
        self.data[key] = value
        self.save()
