r"""
OctaveLights main entry point.
Single-instance enforcement, global exception handling, graceful shutdown.
"""

import sys
import os
import atexit
import signal
import ctypes
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt

from gui import OctaveLightsWindow
from config import Config
from logger import Logger
from midi_listener import MIDIListener
from octave_engine import OctaveEngine
from hid_driver import HIDDriver


def enforce_single_instance():
    """Windows mutex-based single-instance enforcement."""
    if sys.platform != "win32":
        return

    SYNCHRONIZE = 0x00100000
    mutex = ctypes.windll.kernel32.CreateMutexW(
        None,
        False,
        "OctaveLights_SingleInstance"
    )

    if ctypes.windll.kernel32.GetLastError() == 183:
        sys.exit(0)


class OctaveLights:
    def __init__(self):
        """Initialize the application."""
        self.logger = Logger()
        self.config = Config()

        self.hid_driver = HIDDriver()
        self.midi_listener = MIDIListener()
        self.octave_engine = OctaveEngine(self.hid_driver)

        self.app = QApplication.instance() or QApplication(sys.argv)
        self.window = OctaveLightsWindow(self.config, self.midi_listener, self.octave_engine)

        self._connect_signals()

        self.app.aboutToQuit.connect(self._shutdown)
        atexit.register(self._cleanup)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        self.logger.info("OctaveLights initialized")

    def _connect_signals(self):
        """Connect GUI signals to backend."""
        self.window.enabled_changed.connect(self._on_enabled_changed)
        self.window.color_changed.connect(self.octave_engine.set_color)
        self.window.highlight_changed.connect(
            lambda enabled, color: self.octave_engine.set_highlight_pressed(enabled, color)
        )

        self.midi_listener.note_on.connect(self._on_note_on)
        self.midi_listener.note_off.connect(self._on_note_off)

    def _on_enabled_changed(self, enabled):
        """Handle enable/disable toggle."""
        if not enabled:
            self.octave_engine.shutdown()
            self.logger.info("OctaveLights disabled")
        else:
            self.logger.info("OctaveLights enabled")

    def _on_note_on(self, pitch, velocity):
        """Handle MIDI note-on."""
        if self.config.get("enabled"):
            self.octave_engine.on_note_on(pitch, velocity)

    def _on_note_off(self, pitch):
        """Handle MIDI note-off."""
        if self.config.get("enabled"):
            self.octave_engine.on_note_off(pitch)

    def _shutdown(self):
        """Graceful shutdown via Qt."""
        self.logger.info("Shutting down...")
        self.octave_engine.shutdown()
        self.midi_listener.close()
        self.hid_driver.close()
        self.logger.info("OctaveLights closed")

    def _cleanup(self):
        """Final cleanup on exit."""
        try:
            self.octave_engine.shutdown()
        except:
            pass

    def _signal_handler(self, signum, frame):
        """Handle system signals."""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self._shutdown()
        sys.exit(0)

    def run(self):
        """Run the application."""
        try:
            self.window.show()
            return self.app.exec()
        except Exception as e:
            self.logger.error(f"Fatal error: {e}")
            QMessageBox.critical(
                None,
                "OctaveLights Error",
                f"An unexpected error occurred:\n\n{str(e)}\n\n"
                "Please check the logs in %APPDATA%\\OctaveLights\\logs\\ for details."
            )
            self._cleanup()
            return 1


def main():
    """Entry point."""
    enforce_single_instance()

    try:
        app = OctaveLights()
        sys.exit(app.run())
    except Exception as e:
        QApplication([]).exec()
        QMessageBox.critical(
            None,
            "OctaveLights Fatal Error",
            f"Failed to start OctaveLights:\n\n{str(e)}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
