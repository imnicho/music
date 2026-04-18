import json
import os
from pathlib import Path

class Config:
    """Settings persistence to %APPDATA%\OctaveLights\config.json"""

    def __init__(self):
        self.config_dir = Path(os.getenv('APPDATA')) / 'OctaveLights'
        self.config_file = self.config_dir / 'config.json'
        self.defaults = {
            'color': '#FF0000',
            'highlight_pressed_key': True,
            'launch_at_startup': False
        }
        self.data = self.load()

    def load(self):
        """Load config from file or return defaults."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return self.defaults.copy()
        return self.defaults.copy()

    def save(self):
        """Write config to file."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def get(self, key, default=None):
        """Get a config value."""
        return self.data.get(key, default)

    def set(self, key, value):
        """Set a config value and save."""
        self.data[key] = value
        self.save()

config = Config()
